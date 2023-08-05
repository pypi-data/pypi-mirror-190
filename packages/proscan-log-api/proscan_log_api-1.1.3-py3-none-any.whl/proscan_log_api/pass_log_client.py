import mmap
import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Generator, List, Literal, Optional, Union

from proscan_log_api.utils import get_folders, get_pass_files


@dataclass
class InterlockEventData:
    header: Optional[List[str]]
    metadata: Optional[List[str]]
    event: Optional[dict]
    pre_events: Optional[List[dict]]
    post_events: Optional[List[dict]]


class PassClient:
    """This Client can be used to query interlock events from the PASS log-files."""

    def __init__(self, root_dir: Union[str, List[str]], folders: str) -> None:
        """Initialize the Client.

        Args:
            root_dir (str): Root dir path that must contain all the folders on the top level.
            folders (str): Folder that should be searched for matching files. Can be provided as list of strings or as comma separated string (intended for use with env variables).
        """
        self.root_dir = root_dir
        self.folders = folders
        self.row_pattern = re.compile(
            r"(-\s+(?P<id>\d+)\s(?P<timestamp>\d+)\s(?P<value>\w+)\s+(?P<signal_type>\w+)\s+(?P<signal_name>\w+)\s+(?P<datetime>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3}.\d{3})\n)"
        )
        self.header_pattern = re.compile(
            r'(?P<log_type>\w+)\s+area=(?P<area>\w+)\s+time=\w+\s(?P<datetime>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s(?P<timezone>\w+)\s\w+\s=\s"(?P<mode>\w+)"\sinScan\s=\s"(?P<inScan>\w+)"'
        )

    def create_mask(self, timestamp: int = None, signal: str = None) -> str:
        """Create the regex string mask to filter out specific events.

        Args:
            timestamp (int, optional): Timestamp of the event that should be returned. Defaults to None.
            signal (str, optional): Signal name of the events that should be returned. Defaults to None.

        Returns:
            str: _description_
        """
        if not timestamp:
            timestamp_str = rb"\d+"
        else:
            timestamp_str = rb"%d" % timestamp
        if not signal:
            signal_str = rb"\w+"
        else:
            signal_str = rb"%s" % signal
        return (
            rb"(-\s+\d+\s%s\s\w+\s+\w+\s+%s\s+\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3}.\d{3}\n*)"
            % (timestamp_str, signal_str)
        )

    def get(
        self,
        area: Literal["MP", "G2", "G3", "O2"],
        signal: Optional[str] = None,
        timestamp: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        return_fields: Optional[
            List[Literal["header", "metadata", "event", "pre_events", "post_events"]]
        ] = None,
    ) -> Generator[InterlockEventData, None, None]:
        """Get the interlock events from the log files.

        Args:
            area (Literal['MP', 'G2', 'G3', 'O2']): Area where the interlock(s) have occured.
            signal (Optional[str], optional): Signal that caused the interlock. Defaults to None.
            timestamp (Optional[int], optional): Exact timestamp of the interlock. Defaults to None.
            start_date (Optional[date], optional): Earliest date at which interlock should be searched. Defaults to None.
            end_date (Optional[date], optional): Latest date until which interlocks should be searched. Defaults to None.
            return_fields (Optional[ List[Literal['header', 'metadata', 'event', 'pre_events', 'post_events']] ], optional): Fields that should be returned. If none all are returned. If List is provided all fields not in list will be None Defaults to None.

        Raises:
            Exception: If neither start_date, end_date nor timestamp are provided an exception is raised.

        Yields:
            Generator[InterlockEventData, None, None]: InterlockEventData object with all fields not specified in return_fields None unless return_fields is None that all fields have values.
        """
        if not (start_date or end_date or timestamp):
            raise Exception(
                "Please provide at least one of timestamp, start_date or end_date!"
            )
        if start_date > end_date:
            tmp = end_date
            end_date = start_date
            start_date = tmp

        if timestamp:
            start_date = end_date = datetime.fromtimestamp(timestamp / 1000000).date()

        files = get_pass_files(
            folders=get_folders(folders=self.folders, area=area),
            start_date=start_date,
            end_date=end_date,
            root_dir=self.root_dir,
        )

        for file in files:

            for event in self.search_file(
                file,
                mask_str=self.create_mask(timestamp=timestamp, signal=signal),
                return_fields=return_fields,
            ):
                yield event

    def search_file(
        self,
        file_path: str,
        mask_str: str,
        return_fields: Optional[
            List[Literal["header", "metadata", "event", "pre_events", "post_events"]]
        ] = None,
    ) -> Generator[InterlockEventData, None, None]:
        """Searches a single file for intelock events.

        Events are filtered by the mask str, which gets integrated into the pattern to filter a specific first line after the dashed line.

        Args:
            file_path (str): File to be searched.
            mask_str (str): Mask to be added to the pattern, used to only query specific events, see get and create_mask for more info.
            return_fields (Optional[ List[Literal['header', 'metadata', 'event', 'pre_events', 'post_events']] ], optional): Fields that should be returned. If none all are returned. If List is provided all fields not in list will be None. Defaults to None.

        Yields:
            Generator[InterlockEventData, None, None]: InterlockEventData object with all fields not specified in return_fields None unless return_fields is None that all fields have values.
        """
        # Combine Pattern with mask string.
        pattern = re.compile(
            rb"(?P<header>#\s*=+\n#\s+.*\n#\s+=+\n*)(?P<pre>(-\s+\d+\s\d+\s\w+\s+\w+\s+\w+\s+\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3}.\d{3}\n*)+)(?:-+\n*)(?P<post>%s(-\s+\d+\s\d+\s\w+\s+\w+\s+\w+\s+\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3}.\d{3}\n*)+)"
            % (mask_str)
        )
        if not return_fields:
            return_fields = ["header", "metadata", "event", "pre_events", "post_events"]

        with open(file_path, mode="r", encoding="utf-8") as file_obj:
            with mmap.mmap(
                file_obj.fileno(), length=0, access=mmap.ACCESS_READ
            ) as mmap_obj:
                # here the compiled pattern gets applied
                events = pattern.finditer(mmap_obj)
                if not return_fields:
                    return_fields = []
                for event in events:
                    group_dir = event.groupdict()
                    pre_event_list = []
                    post_event_list = []
                    if "pre_events" in return_fields or not return_fields:
                        for row in self.row_pattern.finditer(
                            group_dir["pre"].decode(encoding="utf-8")
                        ):
                            pre_event_list.append(row.groupdict())
                    if (
                        "post_events" in return_fields
                        or "event" in return_fields
                        or "meatdata" in return_fields
                        or not return_fields
                    ):
                        for row in self.row_pattern.finditer(
                            group_dir["post"].decode(encoding="utf-8")
                        ):
                            post_event_list.append(row.groupdict())

                    if post_event_list:
                        event = post_event_list.pop(0)
                    yield InterlockEventData(
                        header=self.header_pattern.search(
                            group_dir["header"].decode(encoding="utf-8")
                        ).groupdict()
                        if "header" in return_fields
                        else None,
                        metadata=list(post_event_list[1].keys())
                        if "metadata" in return_fields
                        else None,
                        event=event if "event" in return_fields else None,
                        pre_events=pre_event_list
                        if "pre_events" in return_fields
                        else None,
                        post_events=post_event_list
                        if "post_events" in return_fields
                        else None,
                    )
