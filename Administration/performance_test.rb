require 'benchmark'

# script which defines two helper methods for measuring and printing out the memory used and time spent.
# Require and loop. Example:
# require_relative './performance_test'
#
# print_memory_usage do
#    print_time_spent do
#        CSV.open("comparison.csv", 'w+') do |csv|
#            puts foo
#        end
#    end
# end
# Credit to: http://dalibornasevic.com/posts/68-processing-large-csv-files-with-ruby


def print_memory_usage
  memory_before = `ps -o rss= -p #{Process.pid}`.to_i
  yield
  memory_after = `ps -o rss= -p #{Process.pid}`.to_i

  puts "Memory: #{((memory_after - memory_before) / 1024.0).round(2)} MB"
end

def print_time_spent
  time = Benchmark.realtime do
    yield
  end

  puts "Time: #{time.round(2)}"
end
