
def site_select()

    puts "[~] Select An Available Site to Generate a Progress Report"
    puts "\nAvailable Sites:"
    puts "_________"
    #sites = @nsc.list_sites
    nameList = ['foo', 'bar']
    nameList.each do |site|
    #sites.each do |site|
        #nameList << site.name.downcase
        #puts site.name
        puts site
    end

    selected = false

    until selected
        print "\n(FULL NAME OF SITE): "
        choice = gets.chomp.downcase
        if nameList.include?(choice)
            selected = choice
        else
            puts "-ERROR- INVALID CHOICE. PLEASE TRY AGAIN."
        end
    end

    puts "You chose #{selected}"
    #return selected
end

site_select()
