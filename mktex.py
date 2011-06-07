#!/usr/bin/env python
# encoding: utf8

import optparse,os

generalhelp = """
Create a latex template file that fulfills some basic requirements
"""

P = optparse.OptionParser(
        usage= "prog [options] <outputfilename>",
        prog = "mktex",
        description = generalhelp
        )

P.add_option("-l","--letter",
    action="store_true",
    help="use letter template")
P.add_option("-m","--math",
    action="store_true",
    help="use amsmath packages")
P.add_option("-a","--article",
    action="store_true",
    help="use article template")
P.add_option("-g","--graphicx",
    action="store_true",
    help="enable graphicx support")
P.add_option("-b","--bibliography",
    default=None,
    help="type of bibliography to be used")
P.add_option("-u","--SIunits",
    action="store_true",
    help="enable SIunits package")
P.add_option("-p","--private",
    action="store_true",
    help="generate a private letter")
P.add_option("-B","--beamer",
        action="store_true",
        help="generate a beamer presentation")

opts,args = P.parse_args()

if len(args)==0:
    P.help()
    os.exit(-1)
else:
    outfilename = args[0]

tex = "\\documentclass[a4paper,11pt]{"
if opts.letter:
    tex += "dinbrief"
elif opts.article:
    tex += "scrartcl"
elif opts.beamer:
    tex += "beamer"
else:
    raise IOError,"No document type requested"
tex += "}\n\n"

if opts.math:
    tex += "\\usepackage{amsmath,amssymb}\n"
    if opts.SIunits:
        tex += "\\usepackage[amssymb]{SIunits}\n"
elif opts.SIunits:
    tex += "\\usepackage[amssymb]{SIunits}\n"

if opts.graphicx:
    tex += "\\usepackage{graphicx}\n"

if opts.bibliography=="apacite":
    tex += "\\usepackage[]{apacite}\n"
elif opts.bibliography==None:
    pass
else:
    tex += "\\usepackage[]{natbib}\n"
    if opts.bibliography in ["newapa"]:
        tex += "\\usepackage{%s}\n" % opts.bibliography

tex += "\\usepackage[utf8]{inputenc}\n"

if opts.letter:
    tex += "\n"
    if opts.private:
        tex += "\\backaddress{Ingo Fründ $\\cdot$ Beusselstr. 88 $\\cdot$ 10553 Berlin}\n"
        tex += "\\address{Ingo Fründ\\\\\n  Beusselstr. 88\\\\\n  10553 Berlin}\n"
    else:
        tex += "\\backaddress{\parbox{7cm}{\\sffamily\\centering "
        tex += "  Ingo Fründ $\\cdot$ TU Berlin $\\cdot$ Fakultät IV\\\\\n"
        tex += "  Sekretariat 6-4 $\\cdot$ Franklinstr. 28/29 $\\cdot$ "
        tex +=    "10587 Berlin}}\n\n"
        if not opts.graphicx:
            tex += "\\usepackage{graphicx}\n"
        tex += "\\address{\n"
        tex += "\\mbox{\\parbox{10cm}{\n"
        tex += "  \\centering\n"
        tex += "  \\textbf{\\LARGE Technische Universität Berlin}\\\\\n"
        tex += "  \\normalsize Arbeitsgruppe Modellierung kognitiver Prozesse\n"
        tex += "  }}\n"
        tex += "  \\flushright\n"
        tex += "  \\parbox{5cm}{\n"
        tex += "    \\begin{center}\n"
        tex += "      \\includegraphics[width=3cm]{/home/ingo/Latex/tu-logo}\n"
        tex += "    \\end{center}\n"
        tex += "    \\scriptsize\\sffamily\n"
        tex += "    Dr. Ingo Fründ\\\\\n"
        tex += "    Technische Universität Berlin\\\\\n"
        tex += "    Modellierung kognitiver Prozesse\\\\\n"
        tex += "    Fakultät IV, Sekretariat 6-4\\\\\n"
        tex += "    Franklinstr. 28/29, 10587 Berlin\\\\\n"
        tex += "    http://www.cognition.tu-berlin.de/\\\\\n"
        tex += "  }\n"
        tex += "}\n\n"
    tex += "\\date{\\today}\n"
    tex += "\\place{Berlin}\n"
    tex += "\\signature{Ingo Fründ}\n"
elif opts.article or opts.beamer:
    tex += "\n"
    tex += "\\title{<++>}\n"
    tex += "\\author{<++>}\n"
    tex += "\\date{<++>}\n"

tex += "\n"
tex += "\\begin{document}\n\n"
if opts.letter:
    tex += "\\begin{letter}{\n  % Recipients address here\n  <++>\n}\n"
    tex += "\\opening{Sehr geehrte Damen und Herren,}\n"
    tex += "% Your text here\n<++>\n"
    tex += "\\closing{Mit freundlichen Grüßen,}\n\n"
    tex += "\\end{letter}\n\n"
elif opts.article:
    tex += "\\maketitle\n"
    tex += "% Your text here\n<++>\n\n"

    if not opts.bibliography == None:
        tex += "\\bibliographystyle{%s}\n" % opts.bibliography
        tex += "\\bibliography{<++>}\n\n"
elif opts.beamer:
    tex += "\\begin{frame}{<++>}\n"
    tex += "% Text here\n"
    tex += "<++>\n"
    tex += "\\end{frame}\n"
tex += "\\end{document}"

outf = open(outfilename,"w")
outf.write(tex)
outf.close()
