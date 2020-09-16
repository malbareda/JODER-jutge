from re import split as resplit
from typing import Union

from dmoj.result import CheckerResult
from dmoj.utils.unicode import utf8bytes

verdict = u"\u2717\u2713"


def check(
    process_output: bytes, judge_output: bytes, point_value: float, feedback: bool = True, **kwargs
) -> Union[CheckerResult, bool]:

    judge_input = list(filter(None, resplit(b'[\r\n]', utf8bytes(kwargs["judge_input"]))))
    process_lines = list(filter(None, resplit(b'[\r\n]', utf8bytes(process_output))))
    judge_lines = list(filter(None, resplit(b'[\r\n]', utf8bytes(judge_output))))
    wronganswers = ""
    

    enjin = [x.decode('utf-8') for x in judge_input]
    strinput = '\n'.join(map(str, enjin))
    print(strinput)


    if len(process_lines) > len(judge_lines):
        while len(process_lines) > len(judge_lines):
            ch = '\u2717'
            ch = ch.encode('utf-8')
            judge_lines.append(ch)
    elif len(process_lines) < len(judge_lines):
        while len(process_lines) < len(judge_lines):
            ch = '\u2717'
            ch = ch.encode('utf-8')
            process_lines.append(ch)

    if not judge_lines:
        return True

    cases = [verdict[0]] * len(judge_lines)
    count = 0

    for i, (process_line, judge_line) in enumerate(zip(process_lines, judge_lines)):
        if process_line.strip() == judge_line.strip():
            cases[i] = verdict[1]
            count += 1
        else:
            tmpl = str(i)+"\u2720"+str(judge_line.strip().decode('utf-8'))+"\u2720"+str(process_line.strip().decode('utf-8'))+"\u2721"
            wronganswers+=(tmpl)


    #Error, so keep the executor exception info
    if kwargs["result_flag"]:
        return CheckerResult(
            count == len(judge_lines), point_value * (1.0 * count / len(judge_lines)), None, strinput+"\u2719"+str(wronganswers)+ "\u2719"+str(len(judge_input))+ "\u2719"+str(len(judge_lines))   )
    #Not an error, so use the new ifno
    else:
        percent = int((count)*100/(len(judge_lines)))
        return CheckerResult(
            count == len(judge_lines), point_value * (1.0 * count / len(judge_lines)), str(percent)+"%" if feedback else "", strinput+"\u2719"+str(wronganswers)+ "\u2719"+str(len(judge_input))+ "\u2719"+str(len(judge_lines))   )
    
check.run_on_error = True  # type: ignore 
