import 'dart:io';

int part_1() {
  final file = new File("input.txt");
  final lines = file.readAsLinesSync();

  final regex = RegExp(r"mul\(\d+,\d+\)");
  var result = 0;

  for (var line in lines) {
    final matches = regex.allMatches(line);
    for (var match in matches) {
      final values = match.group(0)!.split(",");
      result += int.parse(values[0].substring(4)) *
          int.parse(values[1].substring(0, values[1].length - 1));
    }
  }

  return result;
}

int part_2() {
  final file = new File("input.txt");
  final lines = file.readAsLinesSync();

  final regex = RegExp(r"mul\(\d+,\d+\)|do\(\)|don't\(\)");
  var result = 0;
  var enabled = true;

  for (var line in lines) {
    final matches = regex.allMatches(line);
    for (var match in matches) {
      final group = match.group(0)!;
      if (group == "do()") {
        enabled = true;
      } else if (group == "don't()") {
        enabled = false;
      } else if (enabled) {
        final values = group.split(",");
        result += int.parse(values[0].substring(4)) *
            int.parse(values[1].substring(0, values[1].length - 1));
      }
    }
  }

  return result;
}

void run<T>(T Function() fn) {
  final start = DateTime.now().microsecondsSinceEpoch;
  final result = fn();
  final duration = DateTime.now().microsecondsSinceEpoch - start;
  print("($duration): $result");
}

void main() {
  stdout.write("part_1 ");
  run(part_1);
  stdout.write("part_2 ");
  run(part_2);
}
