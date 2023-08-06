# git-timemachine

A command-line tool to help you manage Git commits at different time nodes.

## Quickstart

1. Install command-line tool `git-timemachine` via command:

    ```shell
    pip install git-timemachine
    ```

2. Initialize configurations for `git-timemachine`:

    ```shell
    git-timemachine config --init
    ```

3. Edit the timestamp for last commit and range of time growth
   in `$HOME/.git-timemachine/config` by any plain text editor.

4. In a Git repository, run the following command to record a commit according
   to the timestamp in configurations:

    ```shell
   git-timemachine commit -m 'A commit from specified time point.'
    ```

5. Grow the timestamp for next commits:
    ```shell
   git-timemachine grow
    ```

## License

Copyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>

The GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).
