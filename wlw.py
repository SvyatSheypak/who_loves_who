#!/usr/bin/env python3
"""This program can tell you who loves who by the sentences it read
either from file or from prompted text.
Multiline input is supported
"""

import argparse
import sys


def get_argparser():
    """Builds and returns a suitable argparser"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--file', nargs=1, type=str,
                        help='Read info from file')
    parser.add_argument('-l', '--line', nargs='+', type=str,
                        help='Read info from promted sentence')
    parser.add_argument('-d', '--describe', action='store_true',
                        help='Get list of all people program\
                              knows something about')
    parser.add_argument('-q', '--question', nargs='+', type=str,
                        help='Ask a program abouta certain person\
                              in form `Who likes X`, `Whom loves X`,\
                              `X hates` or simply `X`')
    parser.add_argument('-e', '--exit', action='store_true',
                        help='exit the program')
    return parser


class RelationsGraph(object):
    """Graph with Names as vertices
    and direcnted edges of 3 types:
    loves/likes/hates
    """
    def __init__(self, graph_dict=None):
        """Initializes graph with a dict given
        or sets it empty by default

        Args:
            graph_dict: {
                name : {
                    action : list(str)
                    }
                }
        """
        if graph_dict is None:
            self.__dict = {}
        else:
            self.__dict = graph_dict

    def add_edge(self, atom):
        """Adds edge from atomic expression

        Args:
            atom (list[string]): [subject, action, object]
        """
        if atom[0] not in self.__dict:
            self.__dict[atom[0]] = {atom[1]: [atom[2]]}
        elif atom[1] not in self.__dict[atom[0]]:
            self.__dict[atom[0]][atom[1]] = [atom[2]]
        else:
            self.__dict[atom[0]][atom[1]] += [atom[2]]

    def __optional_passive(self, action, reverse):
        """If reverse == True, transformes a verb to passive voice"""
        if reverse:
            return "is {}d by".format(action[:-1])
        else:
            return action

    def __smart_commas(self, arr):
        """Converts list(str) to a single string with formatting:
        [A, B, C] -> 'A, B and C'
        """
        if len(arr) > 1:
            return ', '.join(arr[:-1]) + ' and ' + arr[-1]
        else:
            return arr[0]

    def get_list_of_people(self):
        """Returns list of vertices"""
        return list(self.__dict.keys())

    def describe_persons_action(self, person, action,
                                reverse=False, short=False):
        """Describes one persons's attitude

        Args:
            person (string): person's name
            action (string): loves/likes/hates
            reverse (bool): special option to interract with reverse graph
            short (bool): option to ommit the subject

        Returns:
            string: verbalization of persons attitude
        """
        if action not in self.__dict[person]:
            if reverse:
                return "No information on who {} {}".format(action, person)
            else:
                return "No information on whom {} {}".format(person, action)

        objects_str = self.__smart_commas(self.__dict[person][action])

        lemmas = [person, self.__optional_passive(action, reverse),
                  objects_str]
        if short:
            lemmas = lemmas[1:]
        output_line = ' '.join(lemmas)
        return output_line.strip()

    def describe_person(self, person, reverse=False):
        """Describes all persons's attitudes

        Args:
            person (string): person's name

        Returns:
            string: verbalization of persons all attitudes
        """
        if person not in self.__dict:
            return ''
        actions = list(self.__dict[person].keys())
        descriptions = [self.describe_persons_action(person, action,
                        reverse, True) for action in actions]
        output_line = person + ' ' + self.__smart_commas(descriptions)
        return output_line


def parse_statement(statement):
    """Converts a complex statement into list of atomic statements

    Args:
        statement (string): a complex statement

    Returns:
        list(list(str)): a list of atomic structures [subject, action, object]
    """
    if not len(statement):
        return []
    simple_text = statement.rstrip('.')
    for word in (',', 'and', 'but'):
        simple_text = simple_text.replace(word, '')

    lemmas = [x.strip() for x in simple_text.split(' ') if len(x.strip())]
    actions = ['loves', 'likes', 'hates']
    cur_subject = lemmas[0]
    cur_action = lemmas[1]
    atoms = []
    for i in range(2, len(lemmas)):
        if lemmas[i] not in actions:
            atoms.append([cur_subject, cur_action, lemmas[i]])
        else:
            cur_action = lemmas[i]
    return atoms


def update_graphs_with_statement(statement, graph, reverse_graph):
    """Update graphs with edges derived from the statement

    Args:
        graph (Graph): relations graph
        reverse_graph (Graph): inverted relations graph
        statement (str): statement to analyze
    """
    atoms = []
    for sentence in statement.split('.'):
        atoms += parse_statement(sentence)
    for atom in atoms:
        graph.add_edge(atom)
        reverse_graph.add_edge(atom[::-1])


def update_graphs_from_file(filename, graph, reverse_graph):
    """Update graphs with edges derived from the statements
    from the file

    Args:
        graph (Graph): relations graph
        reverse_graph (Graph): inverted relations graph
        filename (str): file with statements to analyze
    """
    with open(filename, 'r') as infile:
        for line in infile.readlines():
            update_graphs_with_statement(line.strip(), graph, reverse_graph)


def answer_question(question, graph, reverse_graph):
    """Derives subject and action from the question and gives
    a verbal answer
    """
    lemmas = [x.strip() for x in
              question.strip().split(' ') if x.strip() != '']
    if lemmas[0].lower() == 'whom':
        if lemmas[1] in ['likes', 'hates', 'likes']:
            action = lemmas[1]
            person = lemmas[2]
        else:
            action = lemmas[2]
            person = lemmas[1]
        print(graph.describe_persons_action(person, action))
    elif lemmas[0].lower() == 'who':
        action = lemmas[1]
        person = lemmas[2]
        print(reverse_graph.describe_persons_action(person, action, True))
    elif len(lemmas) == 2:
        action = lemmas[1]
        person = lemmas[0]
        print(graph.describe_persons_action(person, action))
    elif len(lemmas) == 1:
        forward = graph.describe_person(lemmas[0])
        backward = reverse_graph.describe_person(lemmas[0], True)
        if len(forward) == 0 and len(backward) == 0:
            print("No info on {}.".format(lemmas[0]))
        elif forward == '' or backward == '':
            print(forward + backward + '.')
        else:
            print('. '.join([forward, backward]) + '.')
    else:
        print("The question is unclear. Try --help")


def process_input(arg_parser, graph, reverse_graph):
    """Waits for multiple inputs and processes them"""
    args = arg_parser.parse_args()
    process_args(args, graph, reverse_graph)
    while True:
        line = input()
        args = arg_parser.parse_args([line])
        process_args(args, graph, reverse_graph)


def process_args(args, graph, reverse_graph):
    """Converts inputs into graph operations"""
    if args.file:
        filename = args.file[0].strip()
        update_graphs_from_file(filename, graph, reverse_graph)
    if args.line:
        statement = ' '.join(args.line).strip()
        update_graphs_with_statement(statement, graph, reverse_graph)
    if args.question:
        question = ' '.join(args.question).strip()
        answer_question(question, graph, reverse_graph)
    if args.describe:
        print("All Subjects: " + ', '.join(graph.get_list_of_people()))
        print("All Objects: " + ', '.join(reverse_graph.get_list_of_people()))
    if args.exit:
        sys.exit(0)


def main():
    parser = get_argparser()
    graph = RelationsGraph()
    reverse_graph = RelationsGraph()
    process_input(parser, graph, reverse_graph)


if __name__ == "__main__":
    main()
