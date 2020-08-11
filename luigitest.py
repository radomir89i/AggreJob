import luigi
import os
from aggrejob.hhparser import parse_hh


PATH = 'output.csv'


class ParseTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(PATH)

    def run(self):
        data = parse_hh()
        # print(data)
        with self.output().open('w') as f:
            f.write(data)
        # parse_hh(self.output())


class UpdateDBTask(luigi.Task):
    def requires(self):
        return ParseTask()

    def run(self):
        with self.input().open('r') as f:
            print(f.read())


if __name__ == '__main__':
    luigi.build([ParseTask(), UpdateDBTask()], local_scheduler=True)
