# No Comment --- Comment any resource on the web!
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from http import HTTPStatus as HTTP

from no_comment.application.use_cases import view_comments
from no_comment.domain.commenting import entities
from no_comment.interfaces.to_http import HttpPresenter


class XmlPresenter(HttpPresenter):
    def __init__(self, content_type: str = "application/xml") -> None:
        self.__status_code: HTTP = HTTP.OK
        self.__headers: dict[str, str] = {"Content-Type": content_type}
        self.__data: str = ""

    def status_code(self) -> int:
        return int(self.__status_code)

    def headers(self) -> dict[str, str]:
        return self.__headers

    def data(self) -> str:
        return self.__data


class StreamAsAtom(view_comments.Presenter, XmlPresenter):
    def __init__(self) -> None:
        super().__init__("application/atom+xml")
        self.__entries: str = ""

    def data(self) -> str:
        return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>Example Feed</title>
    <link href="http://example.org/"/>
    <updated>2003-12-13T18:30:02Z</updated>
    <author>
        <name>John Doe</name>
    </author>
    <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
    {self.__entries}
</feed>"""

    def comment(self, comment: entities.Comment) -> None:
        self.__entries += f"""
    <entry>
        <title></title>
        <link href="{comment.url}"/>
        <id>ID</id>
        <updated>2023-01-07T16:00:00Z</updated>
        <summary>{comment.text}</summary>
    </entry>
        """


class StreamAsRss(view_comments.Presenter, XmlPresenter):
    def __init__(self) -> None:
        super().__init__("application/rss+xml")
        self.__items: str = ""

    def data(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
    <channel>
        <title>TITLE</title>
        <link>URL</link>
        <description>DESCRIPTION</description>
        {self.__items}
    </channel>
</rss>"""

    def comment(self, comment: entities.Comment) -> None:
        self.__items += f"""
        <item>
            <title></title>
            <link>{comment.url}</link>
            <description>{comment.text}</description>
        </item>
        """
