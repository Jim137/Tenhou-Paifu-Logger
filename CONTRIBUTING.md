# CONTRIBUTING TO Tenhou-Paifu-Logger

## OPENING AN ISSUE

If you have encountered a bug or have a feature request, please open an issue and fill in the template. This will help us to understand your problem and solve it faster.

### FAQ

1. Where did the logs go?
   - The logs are stored in the `Paifu` folder in the same directory as the executable if you don't specify the path.
   - Use `--output [path]` to specify the path to store the logs.
   - If you used pip to install the PaifuLogger, the logs are stored in the `Paifu` folder where the command line opened.
2. There are new elements in the log file that makes the tables broken. Or, it raised `KeyError`. What should I do?
   - Use `--remake` to remake the log file.

## Developer’s Guide

To run Tenhou-Paifu-Logger as a developer, you need to install the dependencies first.

```shell
pip install -r requirements.txt
pip install -r requirements_develop.txt
```

Then you can run the program with

```shell
python -m paifulogger (plog/pdl) [options]
```

### Adding a new feature

If you want to add a new feature, please make a feature request first, tell us what you want to add and you are willing to do it.
Then you can follow the steps below to add the feature.

1. [Fork this repository](https://github.com/Jim137/Tenhou-Paifu-Logger/fork)
2. Checkout the source code with:
   ```shell
   git clone git@github.com:YOUR_GITHUB_USERNAME/Tenhou-Paifu-Logger.git
   ```
3. Start a new branch with:
   ```shell
   cd Tenhou-Paifu-Logger
   git checkout -b BRANCH_NAME
   ```
4. Make your changes.
5. Run unitest with:
   ```shell
   python -m unittest
   ```
   To make sure that your changes don't break the program and all the tests pass.
6. Commit your changes with:
   ```shell
   git add [WHAT YOU CHANGED]
   git commit -m "What you have done"
   ```
7. Push your changes with:
   ```shell
   git push origin BRANCH_NAME
   ```
8. Finally, [create a pull request](https://help.github.com/articles/creating-a-pull-request). We will then review and merge it.

In any case, thank you very much for your contributions!
