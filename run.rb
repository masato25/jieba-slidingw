limit = Time.new("2015","02","12").to_i

base = Time.new("2015","02","07").to_i

while base < limit
  dbase = Time.at(base).strftime "%Y %m %d"
  puts dbase
  flag = system("ruby gen_wddict.rb #{dbase}")
  puts "ok" if flag
  base += 86400
end
