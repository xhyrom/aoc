def check(nums : Array(Int32)) : Bool
  last_operation = -1

  (0...nums.size - 1).each do |i|
    r = nums[i] - nums[i + 1]
    return false if !(3 >= r.abs >= 1)

    operation = r > 0 ? 0 : 1
    return false if last_operation != -1 && last_operation != operation

    last_operation = operation
  end

  true
end

def part_1
  result = 0

  File.read("input.txt").lines.each do |line|
    nums = line.split.map(&.to_i)
    result += 1 if check(nums)
  end

  return result
end

def part_2
  result = 0

  File.read("input.txt").lines.each do |line|
    nums = line.split.map(&.to_i)
    (-1..nums.size - 1).each do |remove|
      copy = nums.dup
      copy.delete_at(remove) if remove >= 0

      if check(copy)
        result += 1
        break
      end
    end
  end

  return result
end

def run(fn)
  start = Time.monotonic.total_nanoseconds
  result = fn.call
  duration = (Time.monotonic.total_nanoseconds - start).to_i64
  puts "(#{duration}): #{result}"
end

print "part_1 "
run ->{ part_1 }
print "part_2 "
run ->{ part_2 }
