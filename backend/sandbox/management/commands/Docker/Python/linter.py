from flake8.api import legacy as flake8

style_guide = flake8.get_style_guide()
report = style_guide.input_file("to_lint.py")
print(report)
print(report.get_statistics("E"))
