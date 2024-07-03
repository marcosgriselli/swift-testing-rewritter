import subprocess
import json
from typing import Optional

def comby_match(pattern: str, extra_args: list[str], extract_holes: list[str]) -> list[dict[str, str]]:
    comby_cmd = ["comby", pattern, "''", "-json-lines", "-matcher", ".swift", "-match-only"]
    comby_cmd.extend(extra_args)
    output = subprocess.check_output(comby_cmd).decode("utf-8")
    if not output:
        print(f"Didn't find any matches for {pattern}")
    
    extracted_matches = _parse_comby_output(output, extract_holes)
    return extracted_matches

def _parse_comby_output(output: str, extract_holes: list[str]):
    # Comby splits the output by lines, so we need to parse each line separately.
    parsed_matches: list[dict[str, str]] = []
    for line in output.splitlines():
        output = json.loads(line)

        matches = output['matches']
        file_path = output['uri']
        if not matches:
            continue

        for match in matches:
            match_dict = {}
            match_dict["matched"] = match["matched"]
            for enviornment in match["environment"]:
                if enviornment["variable"] in extract_holes:
                    match_dict[enviornment["variable"]] = enviornment["value"].strip()
            
            match_dict["file_path"] = file_path # This can be used for the whole match but doesn't hurt here.
            parsed_matches.append(match_dict)

    return parsed_matches    

def comby_rewrite(string: str, pattern: str, replacement: str, extra_args: list[str]) -> Optional[str]:
    comby_cmd = ["comby", pattern, replacement, "-matcher", ".swift", "-stdin", "-stdout"]
    comby_cmd.extend(extra_args)
    input_text = string
    try:
        output = subprocess.check_output(comby_cmd, input=input_text, text=True)
        return output
    except Exception as e:
        print(f"Failed to run comby replacement: {comby_cmd}")
        print(f"Error: {e}")


def comby_rewrite_in_file(pattern: str, replacement: str, extra_args: list[str]) -> Optional[str]:
    comby_cmd = ["comby", "-i", pattern, replacement, "-matcher", ".swift"]
    comby_cmd.extend(extra_args)
    try:
        subprocess.run(comby_cmd)
    except Exception as e:
        print(f"Failed to run comby replacement: {comby_cmd}")
        print(f"Error: {e}")