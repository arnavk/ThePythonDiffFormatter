# ThePythonDiffFormatter

A terrible hack to PEP8 format diffs of Python files. This is really really bad but it works for me.


## WHAT?! WHY?! HOW?!

For a variety of reasons, the repos I work on most often have taken liberties and ignored PEP8 in some places. I want my edits to be compliant so I'd like an autoformatter turned on. However, when I do that, my change set becomes larger than it is because the autoformatters format entire files. So, I hacked this together by combining the functionality of two of the plugins I use:

1. [GitGutter](https://github.com/jisaacks/GitGutter)
2. [Python PEP8 Autoformat](https://bitbucket.org/StephaneBunel/pythonpep8autoformat/src)

It finds the change set using utility methods in GitGutter and then uses the `--line-range` flag on AutoPEP8 to format only the changeset.


## How does this even work?

You need to install [GitGutter](https://github.com/jisaacks/GitGutter) and [Python PEP8 Autoformat](https://bitbucket.org/StephaneBunel/pythonpep8autoformat/src). Yes, I know that isn't ideal and in a future version, I'd like this project to be completely standalone. I hope to get to that when I have some free time (Contributions welcome). Until then, this project will stand on the shoulders of these giants. It would not have been possible without them. 

