package main

import (
	"fmt"
	"os"
	"strings"
	_ "unsafe"
)

type Point struct {
	r, c int
}

func isValid(r, c int, grid []string) bool {
	return r >= 0 && r < len(grid) && c >= 0 && c < len(grid[0])
}

func getAntennas(grid []string) map[rune][]Point {
	antennas := make(map[rune][]Point)

	for r, row := range grid {
		for c, cell := range row {
			if cell != '.' {
				antennas[cell] = append(antennas[cell], Point{r, c})
			}
		}
	}

	return antennas
}

func combinations(arr []Point) [][2]Point {
	var result [][2]Point

	for i := 0; i < len(arr); i++ {
		for j := i + 1; j < len(arr); j++ {
			result = append(result, [2]Point{arr[i], arr[j]})
		}
	}

	return result
}

func part_1() int {
	data, _ := os.ReadFile("input.txt")
	grid := strings.Split(strings.TrimSpace(string(data)), "\n")
	antinodes := make(map[Point]bool)

	for _, positions := range getAntennas(grid) {
		for _, pair := range combinations(positions) {
			r1, c1 := pair[0].r, pair[0].c
			r2, c2 := pair[1].r, pair[1].c

			p1 := Point{2*r2 - r1, 2*c2 - c1}
			p2 := Point{2*r1 - r2, 2*c1 - c2}

			if isValid(p1.r, p1.c, grid) {
				antinodes[p1] = true
			}

			if isValid(p2.r, p2.c, grid) {
				antinodes[p2] = true
			}
		}
	}

	return len(antinodes)
}

func part_2() int {
	data, _ := os.ReadFile("input.txt")
	grid := strings.Split(strings.TrimSpace(string(data)), "\n")
	antinodes := make(map[Point]bool)

	for _, positions := range getAntennas(grid) {
		for _, pair := range combinations(positions) {
			r1, c1 := pair[0].r, pair[0].c
			r2, c2 := pair[1].r, pair[1].c

			directions := [][4]int{
				{r2 - r1, c2 - c1, r1, c1},
				{r1 - r2, c1 - c2, r2, c2},
			}

			for _, dir := range directions {
				dr, dc, r, c := dir[0], dir[1], dir[2], dir[3]
				for isValid(r, c, grid) {
					antinodes[Point{r, c}] = true
					r += dr
					c += dc
				}
			}
		}
	}

	return len(antinodes)
}

//go:linkname nanotime runtime.nanotime
func nanotime() int64

func run[T any](fun func() T) {
	start := nanotime()
	result := fun()
	duration := nanotime() - start
	fmt.Printf("(%d): %v\n", duration, result)
}

func main() {
	fmt.Print("part_1 ")
	run(part_1)
	fmt.Print("part_2 ")
	run(part_2)
}
