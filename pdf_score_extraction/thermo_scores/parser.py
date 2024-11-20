# stdlib
import re
import json
import subprocess
import pathlib
from typing import Dict, List, Union, cast

# 3rd party
# ---------

# local
# -----


def pdf_to_json_scores(
    src: Union[str, pathlib.Path],
    dst: Union[str, pathlib.Path] = None,
    ignore_exceptions: bool = True,
) -> pathlib.Path:
    """Extracts risk scores from the given PDF and writes to scores to a file.

    Args:
        src (Union[str, pathlib.Path]): Path to the PDF file from which to extract
            risk scores.
        dst (Union[str, pathlib.Path], optional): The JSON file to write scores to.
            If None the filename is determined from the PDF filename. Defaults to None.
        ignore_exceptions (bool, optional): If False an exception is raise when risk
            scores are not found. Defaults to True.

    Returns:
        pathlib.Path: The JSON file containing the risk scores.
    """
    src = pathlib.Path(src).expanduser().resolve()
    dst = (
        src.with_suffix(".json")
        if dst is None
        else pathlib.Path(dst).expanduser().resolve()
    )

    content = pdf_to_string(src)
    scores = extract_scores(content, ignore_exceptions=ignore_exceptions)

    with open(dst, "w") as f:
        json.dump(scores, f)

    return dst


def pdf_to_string(src: Union[str, pathlib.Path]) -> str:
    """Extracts the contents of the given PDF to a string.

    Args:
        src (Union[str, pathlib.Path]): Path to the pdf file.

    Returns:
        str: The result of calling 'pdf2txt.py' on the pdf referenced by ``src``.
    """
    src = pathlib.Path(src).expanduser().resolve()
    content = subprocess.check_output(["pdf2txt.py", "-t", "text", src])
    return content.decode("utf-8")


def extract_scores(content: str, ignore_exceptions: bool = True):
    """Extracts the risk scores associated with the left/right breasts.

    Args:
        content (str): The content of the PDF report in the form of a string, namely,
            the output of pdf_to_string.

    Raises:
        ValueError: If either the left or right (or both) breast scores are not found.

    Returns:
        dict of dict: The top level dictionary has two keys, one of each breast, the
        sub-dictionaries (associated to each breast) contain the score information
        for their respective breasts. The resulting dictionary is of the form:

        .. code-block:: python
           {
               "left_breast": {
                   "level_string": "TH-2",
                   "level": "2",
                   "score": "45"
               },
               "right_breast": {
                   "level_string": "TH-2",
                   "level": "2",
                   "score": "35"
               }
           }
    """
    # Designed to match:
    #     "Left Breast: TH-2, Score = 45"
    #     "Left Breast: TH-M"
    lb_regex = r"Left Breast\s*:\s*(?P<level_string>TH-(?P<level>[1-5A-Z]+))(,\s*[sS]core\s*=\s*(?P<score>[0-9]+))?"
    rb_regex = r"Right Breast\s*:\s*(?P<level_string>TH-(?P<level>[1-5A-Z]+))(,\s*[sS]core\s*=\s*(?P<score>[0-9]+))?"

    # Designed to return the segments of document containing the impressions
    lb_locale_regex = r"Left Breast\s*:(.*?)Discussion\s*:"
    rb_locale_regex = r"Right Breast\s*:(.*?)Left Breast\s*:"

    try:
        _BreastScoreType = Dict[str, Union[str, List[str]]]

        lb_groupdict = re.search(lb_regex, content).groupdict()
        lb_groupdict = cast(_BreastScoreType, lb_groupdict)  # help with type hinting
        lb_groupdict["impressions"] = impression_strings(content, lb_locale_regex)

        rb_groupdict = re.search(rb_regex, content).groupdict()
        rb_groupdict = cast(_BreastScoreType, rb_groupdict)  # help with type hinting
        rb_groupdict["impressions"] = impression_strings(content, rb_locale_regex)

        scores = {"left_breast": lb_groupdict, "right_breast": rb_groupdict}
        return scores
    except AttributeError as e:
        if not ignore_exceptions:
            raise ValueError("Unable to find scores") from e


def impression_strings(content: str, locale_regex: str) -> List[str]:
    """Extracts impressions from the some content.

    Args:
        content (str): The extracted PDF content.
        locale_regex (str): The (multiline) regex used to extract the subsection of
            ``content`` which contains impressions for either the left or right breast.
            The resulting string is then searched by the 'impression regex', namely,
            r"\\s*(?P<impression>.*)". A list of all matching strings are then returned.

    Returns:
        List[str]: The impressions
    """
    impression_regex = r"\s*(?P<impression>.*)"

    locale = re.search(locale_regex, content, re.DOTALL).group(1)
    matches_dicts = [s.groupdict() for s in re.finditer(impression_regex, locale)]
    impressions = [d["impression"].strip() for d in matches_dicts]

    return impressions


def pdf_to_txt(
    src: Union[str, pathlib.Path], dst: Union[str, pathlib.Path]
) -> pathlib.Path:
    """Extracts the contents of the given PDF and writes it to a file.

    Args:
        src (Union[str, pathlib.Path]): Path to the pdf file.
        dst (Union[str, pathlib.Path]): Path to the txt file to write to.

    Returns:
        pathlib.Path: Path to the txt file.
    """
    src = pathlib.Path(src).expanduser().resolve()
    dst = pathlib.Path(dst).expanduser().resolve()
    content = pdf_to_string(src)
    dst.write_text(content, encoding="utf-8")
    return dst
