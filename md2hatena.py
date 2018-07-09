import argparse
import re
import os
parser = argparse.ArgumentParser(description='markdown 2 hatena')
parser.add_argument('--input',"-i", type=str,default="input.md",
                    help='input file')
parser.add_argument('--output',"-o", type=str,default="output.md",
                    help='ouput file')
args = parser.parse_args()

inline_flag = 0
block_flag = 0
lines = []
g = open(args.output,"w",encoding="utf-8_sig")
def escape(line):
    line = line.replace("_","\_")
    line = line.replace("^","\^")
    line = line.replace("\\{","\\\\{")
    line = line.replace("\\}","\\\\}")
    return line
"""
read file and split by math symbol $$ or $
"""
# OSの考慮
enc = "utf-8" if os.name == "posix" else "utf-8_sig"
with open(args.input,encoding=enc) as f:
    for line in f:
        if line.find("$$") > -1:
            seps = line.split("$$")
            for i,sep in enumerate(seps):
                # $$ だけの行の場合は空と改行コードだけに分割されるため、その考慮
                if sep == "\n":
                    continue
                # $$ で別れた最終行,元から改行コードが入るためこちらではいれず.
                if i+ 1 ==  len(seps):
                    lines.append(sep)
                else:
                    lines.append(sep + "$$" + "\n")
        elif line.find("$") > -1:
            # $$ で別れた最終行,元から改行コードが入るためこちらではいれず.
            seps = line.split("$")
            for i,sep in enumerate(seps):
                if i+ 1 ==  len(seps):
                    lines.append(sep)
                else:
                    lines.append(sep + "$" + "\n")
        else:
            lines.append(line)


    table_flag = 0
    for line in lines:
        table_st = line.find("|:-")
        # table の終わりの運用で検知して止める.
        table_end = line.find("|||")
        start_d = line.find("$")
        start_dd = line.find("$$")
        start_math =  line.find("```math")
        end_math =  line.find("```")
        para_word = line.find("#")
        # block flagは$$数式の中の意味
        if para_word == 0:
            line = "##" + line
        if start_dd > -1 and block_flag == 0:
            block_flag = 1
            w_line = line[:start_dd] + "[tex: { \displaystyle" + escape(line[start_dd+2:])
        elif start_dd > -1:
            block_flag = 0
            w_line = escape(line[:start_dd]) + "}]" + line[start_dd+2:]
        elif start_math > -1:
            block_flag = 1
            w_line = line[:start_math] + "[tex: { \displaystyle" + escape(line[start_math+7:])
        elif end_math > -1 and block_flag:
            block_flag = 0
            w_line = escape(line[:start_math]) + "}]" + line[start_math+3:]
        elif start_d > -1 and inline_flag == 0:
            inline_flag = 1
            w_line = line[:start_d] + "[tex: {" + escape(line[start_d+1:])
        elif start_d > -1:
            inline_flag = 0
            w_line = escape(line[:start_d]) + "}]" + line[start_d+1:]
        elif inline_flag or block_flag:
            w_line = escape(line)
            print("OK")
        else:
            w_line = line
        #if w_line.find("\{") > -1:
        #    import IPython;IPython.embed()
        if table_st > -1:
            table_flag = 1
            print("tablest",table_flag)
        if table_end > -1:
            table_flag = 0
            w_line = w_line.replace("|||","|")
        if  (table_flag and table_st == -1) or inline_flag :
            # table内は一行にまとめる. 
            print("yay")
            #import IPython;IPython.embed()
            g.write(w_line[:-1])
        else:
            g.write(w_line)
g.close()
