# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyassignment',
 'pyassignment.actions',
 'pyassignment.assignment',
 'pyassignment.assignment.answers',
 'pyassignment.filters',
 'pyassignment.graders',
 'pyassignment.question_bank',
 'pyassignment.readers',
 'pyassignment.writers']

package_data = \
{'': ['*']}

install_requires = \
['macro-expander>=0.3,<0.4',
 'numpy>=1.24.1,<2.0.0',
 'pint>=0.20.1,<0.21.0',
 'pyerrorprop>=3.1.2,<4.0.0',
 'pylatex>=1.4.1,<2.0.0',
 'pyparsing>=3.0.9,<4.0.0',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'pyassignment',
    'version': '2.0.1',
    'description': 'A python module for authoring and assessing homework assignments.',
    'long_description': '# `pyAssignment`\n\nA python module for authoring homework assignments and assessments.\n\n# Description\n\nThis is a rewrite of the [`pyHomework`](https://github.com/CD3/pyHomework) module, which was created to help\nwrite homework assignments for physics classes. The rewrite is currently in progress.\n\n## Features\n\n- Build assignments and compute solutions in pure Python.\n    - Output assignment to LaTeX and build a PDF.\n    - Output assignment to a Blackboard quiz.\n    - Create problem set / Blackboard quiz pair. I.e. a Blackboard quiz that asks questions about\n      a problem set distributed as PDF.\n- [`pyErrorProp\'](https://github.com/CD3/pyErrorProp) integration. Tolerances for numerical solutions\n  can be automatically calculated using error propagation.\n\n## Installing\n\nTo install `pyAssignment`, code this repository and use `pip` to install.\n\n```bash\n$ git clone https://github.com/CD3/pyAssignment\n$ cd pyAssignment\n$ pip install .\n```\n\n\n`pyAssignment` depends on the following modules available on PyPi, which you will need to install with `pip`.\n\n- pytest\n- markdown-to-json\n- numpy\n- Pint\n- PyLaTeX\n- pyparsing\n- PyYAML\n\n\nIn addition to these, you will need to install `macro_expander`\n\n```bash\n$ pip install git+https://github.com/CD3/macro_expander\n```\n\nOptionally, if you want to do error propagation (which is very useful), you will need to install `pyErrorProp`\n\n```bash\n$ pip install git+https://github.com/CD3/pyErrorProp\n```\n\nYou will also need a LaTeX installation, such as texlive, with `pdflatex` to use the LaTeX writer.\n\n## Examples\n\nMy primary use case for `pyAssignment` is writing a Physics homework set. I want to create a PDF that contains\nproblems that the students must work, and then I want to create a Blackboard quiz for the students to complete\nthat asks questions about the problem set. The Blackboard quiz will typically contain some multiple choice questions\nand several numerical answer questions, where the students must compute a numerical value for one of the problems\nin the problem set and enter their answer into the quiz.\n\nThe basic procedure for create this type of assignment is to\n\n1. Create an object of the `Assignment` class.\n1. Add questions to the assignment with the `add_question()` method of the assignment object.\n1. Add parts to a question with the `add_part()` method of the question object.\n1. Add quiz questions for a question or part with the `add_question()` method of the question object.\n1. Add an answer to the quiz question with the `add_answer()` method of the quiz question object.\n\nHere is a basic working example\n\n```python\nimport os,sys\nfrom pyAssignment.Assignment import Assignment\nimport pyAssignment.Assignment.Answers as Answer\nfrom pyAssignment.Actions import BuildProblemSetAndBlackboardQuiz\nimport pint\n\nunits = pint.UnitRegistry()\nQ_ = units.Quantity\n\nass = Assignment()\nass.meta.title = r\'Simple Assignment\'\n\nwith ass.add_question() as q:\n  q.text = r\'\'\'Calculate the weight of a 20 kg mass.\'\'\'\n\n  with q.add_question() as qq:\n    qq.text = r\'\'\'What is the mass?\'\'\'\n    with qq.add_answer(Answer.Numerical) as a:\n      a.quantity = (Q_(20,\'kg\')*Q_(9.8,\'m/s^2\')).to(\'N\')\n\n\nbasename = os.path.basename(__file__).replace(".py","")\nBuildProblemSetAndBlackboardQuiz(ass,basename)\n\n```\n\nThe `BuildProblemSetAndBlackboardQuiz` function is an "action". It takes an assignment object and creates a PDF containing\nthe assignment questions, and any parts that the questions might have. Questions contained in each question or part\nare extracted and written to a text file that is suitable for uploading directly into a Blackboard quiz.\nBoth files are written to a sub-directory named `_<BASENAME>`, where\n`<BASENAME>` is the basename of the assignment file. For example, if the\nassignment file is named `BasicAssignment.py`, then the PDF and Blackboard quiz\nfile will be named `_BasicAssignment/BasicAssignment.pdf` and\n`_BasicAssignment/BasicAssignment-quiz.txt`, respectivly.\n\n\n[Here](./doc/examples/_BasicAssignment/BasicAssignment.pdf) is the PDF that gets generated.\n\n[Here](./doc/examples/_BasicAssignment/BasicAssignment-quiz.txt) is the Blackboard quiz file that gets generated.\n\nA couple of things to note about the Blackboard quiz:\n\n1. `pyAssignment` automatically determines what problem number each quiz question corresponds to and inserts a statement\n   "For problem #X: " at the beginning of each question. This was actually the original motivation for creating `pyHomework`.\n   I wanted a way to write quizzes for homework assignments that could be automatically graded and did not require me to\n   restate a bunch of information from the problem set. In order to do this, each quiz question needed to reference a specific\n   problem number. Doing this manually can be error-prone, as you can imagine...\n1. `pyAssignment` automatically detects the units for a numerical answer and inserts a statement "Give your answer in X." at\n   the end of each question text. Blackboard only accepts numerical values, its not possible to specify the units in your answer,\n   so the quiz question must indicate to the student what units their answer is to be expressed in. Otherwise, students\n   will say "Well, I computed the answer in Y. I think its the same thing as X, can you please check this?".\n1. `pyAssignment` automatically computes a tolerance for the numerical answer. If no estimate of error\n   is given (i.e. you don\'t specify uncertainties in your input values), then `pyAssignment` will use 1%. It is also\n   possible to have the tolerance directly computed using error propagation (using the [`pyErrorProp\'](https://github.com/CD3/pyErrorProp) module). However, `pyAssignment`\n   will always use at least a 1% tolerance, even if the actual uncertainty is compted to be less. This lets the students\n   safely round their answer to three significant figures when they enter it into Blackboard.\n',
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
