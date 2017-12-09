import io
import re
import os.path

line_type_require = "require"
line_type_empty_line = "empty_line"
line_type_func_declare = "func_declare"
line_type_return = "return"
line_type_func_invoke = "func_invoke"
line_type_inserted = "inserted"
line_type_edited = "edited"
line_type_M = "_M"


def require_detector(line):
    # print("require_detector: ", line)
    pattern = re.compile("require")
    match = pattern.search(line)
    if match:
        return True
    else:
        return False


def empty_line_detector(line):
    return len(line) <= 0


def func_declare_detector(line):
    pattern = re.compile("function [.\s_\w\d]+\([\w\,\s]*\)")
    match = pattern.search(line)
    if match is None:
        return False
    else:
        return True


def return_detector(line):
    pattern = re.compile("return[\s_\w\d]+")
    match = pattern.search(line)
    if match is None:
        return False
    else:
        return True


def func_invoke_detector(line):
    pattern = re.compile("local [\s_\w\d,]+\=[\s_\w\d,.:]+\([\w\",_\s]+\)")
    match = pattern.search(line)
    if match is None:
        return False
    else:
        return True


def module_return_detector(line):
    if line.find("return _M") >= 0:
        return True
    else:
        return False


line_type_detector = {
    line_type_require: require_detector,
    line_type_empty_line: empty_line_detector,
    line_type_func_declare: func_declare_detector,
    line_type_M: module_return_detector,
    line_type_return: return_detector,
    line_type_func_invoke: func_invoke_detector,
}


def read_lines_of_file(file_full_path):
    with io.open(file_full_path) as f:
        lines = f.readlines()
        return lines


def judge_line_type(line):
    # line = line.replace('\n', '')
    for key in line_type_detector:
        if line_type_detector[key](line) is True:
            return key
    return "unknown"


def detect_type_info_of_lines(lines):
    info_of_lines = []
    line_num = 1
    for line in lines[:]:
        cleared = line.replace('\n', '')
        line_type = judge_line_type(cleared)
        info_of_lines.append({"raw_line_num": line_num, "line_type": line_type, "content": cleared})
        line_num = line_num + 1
    return info_of_lines


def generate_debug_info_func_declare(line_info, ops=None):
    clear_prefix = line_info["content"].replace("local ", "").replace("function ", "")
    func_name = clear_prefix[:clear_prefix.find("(")]
    paras = clear_prefix[clear_prefix.find("(") + 1:clear_prefix.find(")")].replace(" ", "")
    if len(paras) > 0:
        para_names = paras.split(",")
        paras_of_debug_info = ""
        for name in para_names:
            if len(paras_of_debug_info) <= 0:
                paras_of_debug_info = "%s = %s" % (name, name)
            else:
                paras_of_debug_info = "%s, %s = %s" % (paras_of_debug_info, name, name)
        new_line = {"line_type": line_type_inserted,
                    "content": '    local debug_info = {desc = "%s", paras = {%s}, details = {}}' % (
                        func_name, paras_of_debug_info)}
    else:
        new_line = {"line_type": line_type_inserted,
                    "content": '    local debug_info = {desc = "%s", details = {}}' % func_name}
    return [line_info, new_line]


def generate_debug_info_return(line_info, ops=None):
    count_of_returned_values = len(line_info["content"].replace("return", "").split(","))
    if count_of_returned_values >= 3:
        return [line_info]
    elif count_of_returned_values == 2:
        new_line = {"line_type": line_type_edited, "content": "%s, debug_info" % line_info["content"]}
        return [new_line]
    elif count_of_returned_values == 1:
        new_line = {"line_type": line_type_edited, "content": "%s, nil, debug_info" % line_info["content"]}
        return [new_line]
    else:
        new_line = {"line_type": line_type_edited, "content": "nil, nil, debug_info"}
        return [new_line]


def generate_debug_info_func_invoke(line_info, ops=None):
    content = line_info["content"]
    # print(content)
    local_vars = content[:content.find("=")].replace("local ", "").replace(" ", "").split(",")
    assert len(local_vars) > 0 and len(local_vars) < 3, "not func invoke code: " + content
    if len(local_vars) is 1:
        paras = "%s, %s" % (local_vars[0], "_")
    else:
        paras = "%s, %s" % (local_vars[0], local_vars[1])

    paras = "%s, %s" % (paras, "detail")

    edited_line = {"line_type": line_type_inserted,
                   "content": content[:content.find("local ") + 6] + paras + content[content.find("="):]}
    new_line = {"line_type": line_type_inserted, "content": "    table.insert(debug_info.details, detail)"}
    return [edited_line, new_line]


def generate_debug_info_require(line_info, ops=None):
    if ops is not None and ops["require_debug_files"] is not None:
        content = line_info["content"]
        pattern = re.compile('\(\"[\w.]+\"\)')
        mathch = pattern.search(content)
        if mathch:
            require_pkg_names = content[mathch.start() + 2: mathch.end() - 2].split(".")
            pkg_name = require_pkg_names[len(require_pkg_names) - 1]
            for debug_file_name in ops["require_debug_files"]:
                if pkg_name == debug_file_name:
                    new_content = content[:mathch.start()] + '("%s_debug")' % (".".join(require_pkg_names))
                    new_line = {"line_type": line_type_edited, "content": new_content}
                    return [new_line]
            return [line_info]
        else:
            return [line_info]
    else:
        return [line_info]


def generate_debug_info(line_info, ops):
    if line_info["line_type"] is line_type_func_declare:
        return generate_debug_info_func_declare(line_info, ops)
    elif line_info["line_type"] is line_type_return:
        return generate_debug_info_return(line_info, ops)
    elif line_info["line_type"] is line_type_func_invoke:
        return generate_debug_info_func_invoke(line_info, ops)
    elif line_info["line_type"] is line_type_require:
        return generate_debug_info_require(line_info, ops)
    else:
        return [line_info]


def save_to_file(lines, debug_file_full_path):
    with io.open(debug_file_full_path, "w") as f:
        for line_info in lines:
            f.write(line_info["content"] + "\n")


def generate_debug_info_of_lines(info_of_lines, ops):
    new_lines = []
    for index, line_info in enumerate(info_of_lines):
        debug_info = generate_debug_info(line_info, ops)
        if debug_info is not None:
            new_lines.extend(debug_info)
    return new_lines


def name_debug_file(src_file_path):
    full_path_pre_and_ext = os.path.splitext(src_file_path)
    debug_file_full_path = full_path_pre_and_ext[0] + "_debug" + full_path_pre_and_ext[1]
    return debug_file_full_path


def generate_debug_file(lines, debug_file_path, ops):
    info_of_lines = detect_type_info_of_lines(lines[:])
    new_lines = generate_debug_info_of_lines(info_of_lines, ops)
    save_to_file(new_lines, debug_file_path)
    return new_lines


def handle_file(src_file_path, ops):
    lines = read_lines_of_file(src_file_path)
    return generate_debug_file(lines, name_debug_file(src_file_path), ops)


def handle_files(src_files, ops):
    for src_file in src_files:
        handle_file(src_file, ops)


if __name__ == '__main__':
    local_full_file_path = "./lua/cluster_conf.lua"
    # local_full_file_path = "./lua/config_by_file.lua"
    ops = {"require_debug_files": ["sku", "config_by_file", "topic"]}
    new_lines = handle_file(local_full_file_path, ops)
