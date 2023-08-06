import os.path
import re
import shutil
import tkinter.messagebox
from os import mkdir
from os.path import *
from pathlib import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
warnings = ""

def createProject(product_path):
    product_name = class_name = Path(product_path).stem
    product_folder_path = product_path.replace(".java", "")
    product_idea_path = product_folder_path + "\\.idea"
    product_src_path = product_folder_path + "\\src"
    if os.path.exists(product_folder_path):
        shutil.rmtree(product_folder_path)
    mkdir(product_folder_path)
    mkdir(product_idea_path)
    mkdir(product_src_path)
    IML_path = product_folder_path + "\\" + product_name + '.iml'
    IML = open(IML_path, 'w')
    IML.write('''<?xml version="1.0" encoding="UTF-8"?>
<module type="JAVA_MODULE" version="4">
  <component name="NewModuleRootManager" inherit-compiler-output="true">
    <exclude-output />
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$/src" isTestSource="false" />
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>''')
    IML.close()
    gitignore_path = product_idea_path + "\\.gitignore"
    gitignore = open(gitignore_path, 'w')
    gitignore.write('''# Default ignored files
/shelf/
/workspace.xml
''')
    gitignore.close()
    misc_path = product_idea_path + "\\misc.xml"
    misc = open(misc_path, 'w')
    misc.write('''<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" languageLevel="JDK_19" default="true" project-jdk-name="openjdk-19" project-jdk-type="JavaSDK">
    <output url="file://$PROJECT_DIR$/out" />
  </component>
</project>''')
    misc.close()
    modules_path = product_idea_path + "\\" + "modules.xml"
    modules = open(modules_path, 'w')
    modules.write('''<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/''' + product_name + '''.iml" filepath="$PROJECT_DIR$/''' + product_name + '''.iml" />
    </modules>
  </component>
</project>''')
    modules.close()
    workspace_path = product_idea_path + "\\" + "workspace.xml"
    workspace = open(workspace_path, 'w')
    workspace.write('''<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ChangeListManager">
    <list default="true" id="8786fb5e-0e17-4943-9edd-ce5c818a7525" name="Changes" comment="" />
    <option name="SHOW_DIALOG" value="false" />
    <option name="HIGHLIGHT_CONFLICTS" value="true" />
    <option name="HIGHLIGHT_NON_ACTIVE_CHANGELIST" value="false" />
    <option name="LAST_RESOLUTION" value="IGNORE" />
  </component>
  <component name="ProjectId" id="2IRbHv13ONTdWo18OqVVevzF5r4" />
  <component name="ProjectViewState">
    <option name="hideEmptyMiddlePackages" value="true" />
    <option name="showLibraryContents" value="true" />
  </component>
  <component name="PropertiesComponent"><![CDATA[{
  "keyToString": {
    "RunOnceActivity.OpenProjectViewOnStart": "true",
    "RunOnceActivity.ShowReadmeOnStart": "true"
  }
}]]></component>
  <component name="SpellCheckerSettings" RuntimeDictionaries="0" Folders="0" CustomDictionaries="0" DefaultDictionary="application-level" UseSingleDictionary="true" transferred="true" />
  <component name="TaskManager">
    <task active="true" id="Default" summary="Default task">
      <changelist id="8786fb5e-0e17-4943-9edd-ce5c818a7525" name="Changes" comment="" />
      <created>1670147259738</created>
      <option name="number" value="Default" />
      <option name="presentableId" value="Default" />
      <updated>1670147259738</updated>
    </task>
    <servers />
  </component>
</project>''')
    workspace.close()
    product_path = product_src_path + "\\" + product_name + ".java"
    return product_path


def outputStreamOptimization(source_path, product_path, str_base_code):
    code_state1_1 = str_base_code.split(";")
    code_state1_2 = ""
    maxline_ = len(code_state1_1)
    maxline1_ = maxline_ - 1
    acu = 1
    for i in range(0, maxline_):

        current_line_ = code_state1_1[i].replace('<<', "<!connect_insertion_stream!>", acu)
        current_line_ = current_line_.replace('>>', "<!connect_extraction_stream!>", acu)

        if maxline1_ == i:
            current_line_ = re.sub('$', "", current_line_)
        else:
            current_line_ = re.sub('$', ";", current_line_)

        code_state1_2 = code_state1_2 + current_line_

    code_state1 = re.sub('cout.*<!connect_insertion_stream!>', "System.out.print(", code_state1_2)
    code_state2 = re.sub('<<', "+", code_state1)
    code_state3 = re.sub('endl', '"\\\\n"', code_state2)
    code_state3_0 = re.sub('ends', '" "', code_state3)
    code_state4 = code_state3_0.split(";")
    code_state5 = ""
    maxline = len(code_state4)
    maxline1 = maxline - 1
    for i in range(0, maxline):

        boolean1 = code_state4[i].find("System.out.print")
        if boolean1 > 0:
            current_line = re.sub('$', ");", code_state4[i])
        else:
            current_line = re.sub('$', ";", code_state4[i])

        if maxline1 == i:
            current_line = re.sub('$', "", code_state4[i])

        code_state5 = code_state5 + current_line
    output_stream_file = open(product_path, 'w')
    output_stream_file.write(code_state5)
    output_stream_file.close()

    return code_state5


def fieldsOptimization(source_path, product_path, str_base_code):
    code_state1 = re.sub('int.*main.*\(\).*\{', "|Field end~key=Xufy98| public static void main(String[] args) {",
                         str_base_code)
    valid_check = code_state1.find("|Field end~key=Xufy98|")
    if valid_check < 0:
        code_state1 = re.sub('int.*main.*\(\).*', "|Field end~key=Xufy98| public static void main(String[] args) ",
                             str_base_code)
    code_state2 = re.sub('return.*0.*;', '', code_state1)
    code_state2 = re.sub('return.*0.*', '', code_state1)
    code_state3 = re.sub('main.*\(\);', 'String[] arg={""};\n main(arg);', code_state2)
    code_state3 = re.sub('main.*\(\) +;', 'String[] arg={""};\n main(arg);',
                         code_state3)  # 2nd condition for prevent anwanted changes
    code_state3_u2 = "<"
    code_state3_u1 = re.search("#.*include.*<.*:.*>", code_state3)
    none_value = re.search("\|key=qjxbwiub8\|", "")
    if code_state3_u1 != none_value:
        code_state3_u2 = code_state3_u1.group(0)
    code_state3_u2_ = code_state3_u2.split('<')
    code_state3_u3 = code_state3_u2_[1].replace('>', "")
    code_state3_u3 = code_state3_u2_[1].replace('\\', "\\\\")
    code_state3_1 = re.sub('#.*include.*<.*:.*>', "// <Warning> '" + code_state3_u3 + "' -import Failed ;", code_state3)
    code_state3_1_0 = re.sub('#.*include.*<.*.*>', '', code_state3_1)
    code_state3_2 = re.sub('using.*namespace.*std.*;', '', code_state3_1_0)
    code_state3_3 = re.sub('std.*::', '', code_state3_2)
    base_class_open = "{field}\n\n\n{classfield}\n\n\npublic class {Untitled}{b1} {field_items}\n\n{main_funcution} {b2}"
    imports_field_ = code_state3_3.split("|Field end~key=Xufy98|")
    temp_field_sep = code_state3_3.split(";")
    imports_only = ""
    field_only = ""

    maxline = len(temp_field_sep)
    for i in range(0, maxline):

        boolean1 = temp_field_sep[i].find("import")
        boolean2 = re.search("\|Field end~key=Xufy98\|", temp_field_sep[i])
        if boolean1 > 0:
            imports_only = imports_only + temp_field_sep[i]
        if boolean1 < 0 and not (boolean2 == "|Field end~key=Xufy98|"):
            field_only = field_only + temp_field_sep[i] + ";"

    field_only = field_only.split("|Field end~key=Xufy98|")
    imports_only = imports_only + "\nimport java.util.*;"  # add here default imports

    class_name = Path(source_path).stem

    main_funcution_body = imports_field_[1]
    field_only_final = re.sub("int .*\(.*\).*;", "", field_only[0])
    field_only_final = re.sub("float .*\(.*\).*;", "", field_only_final)
    field_only_final = re.sub("string .*\(.*\).*;", "", field_only_final)
    field_only_final = re.sub("char .*\(.*\).*;", "", field_only_final)
    field_only_final = re.sub("short .*\(.*\).*;", "", field_only_final)
    field_only_final = re.sub("double .*\(.*\).*;", "", field_only_final)
    field_only_final = re.sub("long .*\(.*\).*;", "", field_only_final)
    field_only_final = re.sub("bool .*\(.*\).*;", "", field_only_final)
    field_only_final = re.sub("void .*\(.*\).*;", "", field_only_final)

    code_state4 = base_class_open.format(field=imports_only, classfield="<!Class Fied key-jsak316!>",
                                         Untitled=class_name, field_items=field_only_final,
                                         main_funcution=main_funcution_body, b1="{", b2="}")

    output_stream_file = open(product_path, 'w')
    output_stream_file.write(code_state4)
    output_stream_file.close()
    return code_state4

variable_type_scope = ""

def inputStreamOptimization(source_path, product_path, str_base_code):
    global globleline
    product_path_file = open(product_path, 'r')
    global variable_type_scope

    code_state1 = ""
    code_state2 = ""
    active_function_d = False
    line_mod = ""
    br_open = 0
    br_close = 0
    start_br_count = False
    re_factor_cin = ""
    data_type_list = ["int", "float", "string", "char", "long", "double", "short", "bool"]
    data_type_corr_fun = ["nextInt()", "nextFloat()", "nextLine()", "next().charAt(0)", "nextLong()", "nextDouble()",
                          "nextShort()", "nextBoolean()"]
    temp_str = ""
    variable_data_type = ""
    boolean11 = 15
    variable_data_type_final = ""
    close_data_type = ""
    re_factor_cin_final = ""
    for line in product_path_file:

        none_value = re.search("\|key=qjxbwiub8\|", "")

        boolean1 = re.search("void.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        boolean1 = re.search("int.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        boolean1 = re.search("float.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        boolean1 = re.search("string.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        boolean1 = re.search("char.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        boolean1 = re.search("long.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        boolean1 = re.search("double.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        boolean1 = re.search("short.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        boolean1 = re.search("bool.*\(.*\).*", line)
        if boolean1 != none_value:
            active_function_d = True

        line_mod = line

        if (br_open - br_close) != 0:
            active_function_d = False

        if active_function_d == True:
            boolean2 = re.search(".*\{.*", line)
            boolean3 = re.search(".*;.*", line)
            boolean4 = line.find(";")
            boolean5 = line.find("{")

            if boolean2 != none_value and boolean3 == none_value:
                active_function_d = False
                line_mod = re.sub("\{", "{\n Scanner cin = new Scanner(System.in);\n", line, 1)
                start_br_count = True

            elif boolean2 != none_value and boolean3 != none_value:
                if boolean4 > boolean5:
                    active_function_d = False
                    line_mod = re.sub("\{", "{\n Scanner cin = new Scanner(System.in);\n", line, 1)
                    start_br_count = True

            if boolean4 >= 0 or boolean5 >= 0:
                active_function_d = False

        if start_br_count == True:
            br_open_ = re.search(".*\{.*", line)

            if br_open_ != none_value:
                br_open = br_open + 1
            br_close_ = re.search(".*\}.*", line)

            if br_close_ != none_value:
                br_close = br_close + 1

        code_state1 = code_state1 + line_mod

        boolean6 = re.search("cin.*<!connect_extraction_stream!>", line)
        if boolean6 != none_value:
            rev_input = line.split(">>")
            rev_input_size = len(rev_input)

            for i in range(0, rev_input_size):
                boolean7 = rev_input[i].isspace()
                if boolean7 != True:
                    if i == rev_input_size - 1 and i != 0:
                        temp_str = rev_input[i].replace(";", "", 1)
                        temp_str = re.sub("\n", "", temp_str)
                        re_factor_cin = re_factor_cin + temp_str + "=cin." + ";" + "\n"
                        temp_str2 = temp_str
                        temp_str = temp_str.replace(" ", "")
                        variable_data_type_final = getVariableDatatype(temp_str, none_value, close_data_type,
                                                                       data_type_corr_fun, line)

                        re_factor_cin_final = re_factor_cin_final + temp_str2 + " = cin." + variable_data_type_final + ";" + "\n"


                    elif i != 0:
                        re_factor_cin = re_factor_cin + rev_input[i] + "=cin." + ";" + "\n"
                        temp_str2 = rev_input[i]
                        temp_str = rev_input[i].replace(" ", "")
                        variable_data_type_final = getVariableDatatype(temp_str, none_value, close_data_type,
                                                                       data_type_corr_fun, line)

                        re_factor_cin_final = re_factor_cin_final + temp_str2 + " = cin." + variable_data_type_final + ";" + "\n"


                    elif i == 0 and i != rev_input_size - 1:
                        temp_str = rev_input[i].split("<!connect_extraction_stream!>")
                        re_factor_cin = re_factor_cin + temp_str[1] + "=cin." + ";" + "\n"
                        temp_str2 = temp_str[1]
                        temp_str = temp_str[1].replace(" ", "")
                        variable_data_type_final = getVariableDatatype(temp_str, none_value, close_data_type,
                                                                       data_type_corr_fun, line)

                        re_factor_cin_final = re_factor_cin_final + temp_str2 + " = cin." + variable_data_type_final + ";" + "\n"


                    else:
                        temp_str = rev_input[i].split("<!connect_extraction_stream!>")
                        temp_str[1] = temp_str[1].replace(";", "", 1)
                        temp_str[1] = re.sub("\n", "", temp_str[1])
                        re_factor_cin = re_factor_cin + temp_str[1] + "=cin." + ";" + "\n"
                        temp_str2 = temp_str[1]
                        temp_str = temp_str[1].replace(" ", "")
                        variable_data_type_final = getVariableDatatype(temp_str, none_value, close_data_type,
                                                                       data_type_corr_fun, line)

                        re_factor_cin_final = re_factor_cin_final + temp_str2 + " = cin." + variable_data_type_final + ";" + "\n"

                    line_mod = re.sub("cin.*<!connect_extraction_stream!>.*;", re_factor_cin_final, line)

            re_factor_cin_final = ""

        code_state2 = code_state2 + line_mod

        variable_type_scope = variable_type_scope + line

    input_stream_file = open(product_path, 'w')
    input_stream_file.write(code_state2)
    input_stream_file.close()
    return code_state2

def getVariableDatatype(temp_str, none_value, close_data_type, data_type_corr_fun, line):
    global warnings
    global variable_type_scope
    data_type_list = ["int", "float", "string", "char", "long", "double", "short", "bool"]
    variable_data_type_final = ""
    temp_str = re.sub("\[.*]", "", temp_str)
    temp_str = ".*" + temp_str + ".*"
    for j in range(0, 8):
        var_format = data_type_list[j] + " " + ".*" + temp_str + ".*;"
        variable_data_type = re.search(var_format, variable_type_scope)

        if variable_data_type != none_value:
            boolean_8 = variable_data_type.group(0)
            boolean_8_list = boolean_8.split(";")
            boolean_8_size = len(boolean_8_list)

            for d in range(0, boolean_8_size):
                boolean_9 = re.search(temp_str, boolean_8_list[d])
                if boolean_9 != none_value:
                    boolean_9Px = boolean_9.group(0)
                    boolean_9x = re.sub(data_type_list[j], "", boolean_9Px)
                    boolean_9xA = re.search(temp_str, boolean_9x)

                if boolean_9 != none_value:

                    boolean9_9 = boolean_9.group(0)
                    boolean9 = re.search(data_type_list[j], boolean9_9)
                    boolean9 = re.search(data_type_list[j], boolean9_9)

                    if boolean9 != none_value and boolean_9xA != none_value:
                        close_data_type = data_type_corr_fun[j]

            variable_data_type_final = close_data_type

    boolean9final = none_value
    for ib in range(0, 8):
        search1 = ".*" + data_type_corr_fun[ib] + ".*"
        boolean9pre_final = re.search(data_type_corr_fun[ib], variable_data_type_final)
        if ib == 3:
            boolean9pre_final = re.search("charAt\(0\)", variable_data_type_final)

        if boolean9pre_final != none_value:
            boolean9final = "not none"

    if boolean9final != none_value:
        return variable_data_type_final
    else:
        warnings = "*Warnings\n"

        var_name_warnings = temp_str.replace(".*", "")
        alt_varible = "nextInt()/*<Warning> If '" + var_name_warnings + "' is not '<int> type' please change manually*/"
        return alt_varible

def keywordLibraryOptimization(source_path, product_path, str_base_code):
    code_state1 = re.sub(r'\bstring\b', "String", str_base_code)
    code_state2 = re.sub(r'\bconst\b', "final", code_state1)
    code_state3 = re.sub(r'\bbool\b', "boolean", code_state2)
    code_state4 = re.sub("exit\(0\)", "System.exit(0)", code_state3)
    # code_state5=re.sub("","",code_state4)

    input_stream_file = open(product_path, 'w')
    input_stream_file.write(code_state4)
    input_stream_file.close()
    return code_state2

def arrayOptimization(source_path, product_path, str_base_code):
    data_type_list = ["int", "float", "String", "char", "long", "double", "short", "boolean"]
    product_path_file_temp = open(product_path, 'r')
    line_num_t = product_path_file_temp.readlines()
    array_cout_t = re.split("\[.*]", str_base_code)
    boolean_l3 = line_num_t
    line_num_t = len(line_num_t)
    product_path_file_temp.close()
    product_path_file = open(product_path, 'r')
    code_state2 = ""
    boolean1_final = ""
    line_num = 0

    for line in product_path_file:
        none_value = re.search("\|key=qjxbwiub8\|", "")

        boolean1cc_1_final = none_value
        mod_line = line

        for i in range(0, 8):
            boolean0_1 = data_type_list[i] + ".*\[.*].*"
            boolean0_cc2 = "\(.*" + data_type_list[i] + ".*\[.*].*\)"
            boolean0_cc2 = re.search(boolean0_cc2, line)
            boolean1 = re.search(boolean0_1, line)

            if boolean1 != none_value:
                boolean1_final = boolean1
            if boolean0_cc2 != none_value:
                boolean1cc_1_final = boolean0_cc2

        if boolean1_final != none_value and boolean1cc_1_final == none_value:
            mod_line_temp = mod_line.split(";")
            maxline = len(mod_line_temp)
            for j in range(0, maxline):
                composite_line = mod_line_temp[j].split(",")
                maxline_2 = len(composite_line)
                for k in range(0, maxline_2):
                    boolean4 = re.search("\[.*]", composite_line[k])
                    if boolean4 != none_value:
                        for l in range(0, 8):
                            boolean5 = re.search(data_type_list[l], mod_line_temp[j])
                            replace_value_pre = re.search("\[.*]", composite_line[k])
                            search_obj = re.sub("\[.*]", "", composite_line[k])

                            search_obj = ".*" + search_obj + ".*\[.*].*"
                            check12 = re.search(".*=.*", search_obj)
                            search_obj_pre_final = search_obj.split("=")

                            if check12 != none_value:
                                search_obj_pre_final[0] = search_obj_pre_final[0].replace(" ", "")
                                search_obj_pre_final[0] = search_obj_pre_final[0] + ".*\[.*]"

                            search_obj_final = re.sub(data_type_list[l], "", search_obj_pre_final[0])

                            if boolean5 != none_value:

                                array_dimension = ""
                                previous_datatype = data_type_list[l]
                                replace_value_final = replace_value_pre.group(0)
                                array_d_count = replace_value_final.count("[")
                                for i in range(0, array_d_count):
                                    array_dimension = array_dimension + "[]"

                                comstr = "" + array_dimension + "= new " + previous_datatype + replace_value_final  # <!arraydeclear key-98329!>
                                replace_value_final = re.sub("\[", "\\[", replace_value_final)

                                boolean_l4 = re.sub("\.\*", "", search_obj_final)
                                boolean_l4 = re.sub(previous_datatype, "", boolean_l4)
                                boolean_l4 = re.sub(" ", "", boolean_l4)
                                boolean_l4 = re.sub("\[", "", boolean_l4)
                                boolean_l4 = re.sub("]", "", boolean_l4)
                                boolean_l4 = re.sub("]", "", boolean_l4)
                                boolean_l4 = boolean_l4.replace("\\", "")

                                boolean_l5 = re.search(previous_datatype, mod_line_temp[j])
                                st_point = boolean_l5.span()[0]
                                ed_point = boolean_l5.span()[1]
                                if st_point > 0:
                                    st_point = st_point - 1

                                st_point_temp = 0
                                final_bool = False
                                for i in mod_line_temp[j]:
                                    if st_point == st_point_temp:
                                        if st_point > 0:
                                            if i != ' ':
                                                final_bool = True
                                    if ed_point == st_point_temp:
                                        if st_point > 0:
                                            if i != ' ':
                                                final_bool = True

                                    st_point_temp += 1
                                if final_bool == False:
                                    replace_value_final_1 = re.sub(previous_datatype, '', composite_line[k])
                                    replace_value_final_1 = re.sub("\t", '', replace_value_final_1)
                                    replace_value_final_1 = re.sub(" ", '', replace_value_final_1)
                                    replace_value_final = re.sub("\[.*]", "", replace_value_final_1)
                                    comstr = replace_value_final + comstr
                                    mod_line = mod_line.replace(replace_value_final_1, comstr)

        code_state2 = code_state2 + mod_line
        line_num += 1
    input_stream_file = open(product_path, 'w')
    input_stream_file.write(code_state2)
    input_stream_file.close()
    return code_state2

def gotoOptimization(product_path, str_base_code):
    source_file = open(product_path, 'r')
    code_state_final = str_base_code
    for line in source_file:
        boolean_1 = re.search(".*goto.*;", line)
        none_value = re.search("\|key=qjxbwiub8\|", "")
        if boolean_1 != none_value:
            semi_list = line.split(";")
            for i in semi_list:
                boolean_2 = re.search(".*goto.*", i)
                if boolean_2 != none_value:
                    label_name = re.sub("goto", "", i)
                    label_name = re.sub(" ", "", label_name)
                    label_name = re.sub("\t", "", label_name)
            code_state_final = re.sub(label_name + ".*:", label_name + ": /* <Warning> Java does not support goto */",
                                      str_base_code)
            code_state_final = re.sub("goto.*" + label_name,
                                      "goto " + label_name + " /* <Warning> Java does not support goto */",
                                      code_state_final)

    input_stream_file = open(product_path, 'w')
    input_stream_file.write(code_state_final)
    input_stream_file.close()
    return code_state_final

def classesOptimization(source_path, product_path, str_base_code):
    code_state1 = ""
    classes = ""
    product_path_file_temp = open(product_path, 'r')
    file_data_str = product_path_file_temp.read()
    product_path_file_temp.close()
    class_body = ""
    readclass = False
    open_br = 0
    close_br = 0
    end_class = False
    mod_line = ""
    all_classes_name_str = ""
    Total_classes = 0
    product_path_file = open(product_path, 'r')
    for line in product_path_file:

        mod_line = line

        none_value = re.search("\|key=qjxbwiub8\|", line)
        boolean1 = re.search(r"\b" + "class" + r"\b", line)
        if boolean1 != none_value:
            class_body = "public "
            boolean2 = re.search("//.*class", line)
            boolean3 = re.search("/\*.*class.*\*/", line)
            boolean4 = re.search('".*class.*"', line)
            boolean_0_4 = re.search("public class .*\{", line)
            if boolean2 != none_value or boolean3 != none_value or boolean4 != none_value or boolean_0_4 != none_value:
                boolean1 = none_value

        if boolean1 != none_value:
            class_name_boolean = line.split(" ")
            class_name = re.sub("\{.*", "", class_name_boolean[1])
            class_name = re.sub("\n", "", class_name)
            class_name = re.sub("\t", "", class_name)
            class_name = re.sub(" ", "", class_name)

            readclass = True

        if readclass == True:
            boolean5 = re.search(".*\{.*", line)
            boolean6 = re.search(".*}.*", line)
            if boolean5 != none_value:
                open_br += 1
            if boolean6 != none_value:
                close_br += 1

            if readclass == True:

                if open_br == close_br and open_br != 0:
                    boolean7 = re.search(";", line)
                    if boolean7 != none_value:
                        line = re.sub(";", "", line, 1)
                        readclass = False
                        end_class = True
            if readclass == True:
                class_body = class_body + line
                mod_line = ""
                code_state1 = code_state1 + mod_line

            if end_class == True:
                class_body = class_body + line + "\n"
                mod_line = ""
                code_state1 = code_state1 + mod_line
                classes += class_body
                end_class = False
                Total_classes += 1
                all_classes_name_str += class_name + ","

        code_state1 = code_state1 + mod_line

    code_state1 = re.sub("<!Class Fied key-jsak316!>", classes, code_state1)
    product_path_file.close()
    # print(code_state1)
    input_stream_file = open(product_path, 'w')
    input_stream_file.write(code_state1)
    input_stream_file.close()

    mod_line = ""
    code_state2 = ""
    all_classes_names = all_classes_name_str.split(",")
    del all_classes_names[-1]
    product_file2 = open(product_path, 'r')
    for line in product_file2:
        mod_line = line
        none_value = re.search("\|key=qjxbwiub8\|", "")

        for class_name_as_i in all_classes_names:
            search_obj = r"\b" + class_name_as_i + r"\b" + " .+;"
            boolean1 = re.search(search_obj, line)
            if boolean1 != none_value:

                split_line = line.split(";")
                for i in split_line:

                    boolean1_0 = re.search(r"\b" + class_name_as_i + r"\b", i)
                    if boolean1_0 != none_value:
                        split_line_comma = i.split(",")
                        c_t = 0
                        for j in split_line_comma:
                            if c_t == 0:
                                boolean2 = re.sub(r"\b" + class_name_as_i + r"\b", "", j)
                                boolean2 = re.sub(" ", "", boolean2)
                                boolean2 = re.sub("\t", "", boolean2)
                                boolean3 = re.search("\(.*\)", boolean2)

                                if boolean3 != none_value:
                                    args_1 = ""
                                    boolean3 = none_value
                                else:
                                    args_1 = "()"
                                boolean2 = re.sub("\(.*\)", "", boolean2)
                                mod_line = re.sub(r"\b" + boolean2 + r"\b",
                                                  boolean2 + " = new " + class_name_as_i + args_1, mod_line)
                            else:
                                boolean0_2 = re.sub(" ", "", boolean2)
                                boolean0_2 = re.sub("\t", "", boolean2)
                                boolean3_ = re.search("\(.*\)", boolean2)

                                if boolean3_ != none_value:
                                    args_2 = ""
                                    boolean3_ = none_value
                                else:
                                    args_2 = "()"
                                mod_line = re.sub(r"\b" + boolean0_2 + r"\b",
                                                  boolean0_2 + " = new " + class_name_as_i + args_2, mod_line)
                                c_t += 1

        code_state2 = code_state2 + mod_line
    product_file2.close()
    product_file2=open(product_path,'w')
    product_file2.write(code_state2)
    return code_state2

def fileStreamsOptimization(product_path, str_base_code):
    pass
