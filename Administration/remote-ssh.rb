#!/usr/bin/env ruby
###########################################################################
#
# [+] Description: Generic net/ssh script for remote command execution
# on a list of hosts via ssh. Handles auth with highline and prints output to a specified csv.
#
# [+] Use Case: updates, log retrieval, monitoring, service restarts, etc.
#
#                       ~ Written by nxkennedy ~
###########################################################################

#******** Usage ********#
# ruby remote-ssh.rb hostlist.csv output.csv
#
#
#**********************#

require 'rubygems'
require 'net/ssh'
require 'highline'
require 'csv'
require 'timeout'



raise "Script requires a src and dest file" unless ARGV.count == 2
raise "Destination File alread exists #{ARGV[1]}" if File.exist?(ARGV[1])
raise "File Does Not Exist #{ARGV[0]}" unless File.exist?(ARGV[0])
@target = ARGV[1]
@src = ARGV[0]

#Auth stuff
cli = HighLine.new
USER = cli.ask("Enter your Username:  ") { |q| q.echo = true }
PASS = cli.ask("Enter your password:  ") { |q| q.echo = false }


# For-ish loop

    CSV.open(@target, "w+") do |csv|
    csv << ["host", "status"]
    File.readlines(@src).each do |line|
    csv_row = [line.chomp]
    begin
    Timeout.timeout(5) do
        Net::SSH.start( line.chomp, USER, :password => PASS ) do |ssh|
            result = ssh.exec!("cat /etc/issue")
            csv_row << result
        end # SSH block
        end # Timeout block
    rescue Errno::ECONNREFUSED  => e
      csv_row << e.message
    rescue Net::SSH::ConnectionTimeout => e
      csv_row << e.message
    rescue Net::SSH::Disconnect => e
      csv_row << e.message
    rescue => e
      csv_row << e.message
    end # Rescue block
    puts csv_row.inspect
    csv << csv_row
end # Src reading
    end # @target opening/closing
