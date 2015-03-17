require 'logger'

@logger = Logger.new("logger/gen_wddict.log", 'daily')

@wd_pool = {}
def addset(data)
  data.each{|l|
    l.chomp!
    w,f,n = l.split(/\s+/)
    if @wd_pool.has_key?(w)
      @wd_pool[w] += 1
    else
      @wd_pool[w] = f.to_i
    end
  }
end

#set the date is yesterday
wd_date = Time.at(Time.now.to_i - 86400).strftime "%Y_%m_%d"
if ARGV.size > 2
  wd_date = ARGV.join("_")
end

@logger.info("python ptt_cut.python #{wd_date}")
flag = system("python ptt_cut.python #{wd_date}")

if flag == true
  wd_pool = {}
  @logger.info("[#{wd_date}] read custom_word.wd")
  if File.exist?('result/dict/custom_word.wd')
    f = File.open('result/dict/custom_word.wd','r')
    wddb = f.read.split(/\n/)
    wleng = wddb.size
    @logger.info("[#{wd_date}] custom_word.wd had #{wleng} words.")
    addset(wddb)
  else
    @logger.warn("custom_word.wd not exiting , skip read. contiune generate new coustom dict.")
  end
  # myear,mmonth,mday = wd_date.split("_")
  # ys_wd_date = Time.at(Time.new(myear,mmonth,mday).to_i - 86400).strftime "%Y_%m_%d"
  if File.exist?("result/newwd/#{wd_date}.wd")
    f = File.open("result/newwd/#{wd_date}.wd","r")
    newf = f.read.split(/\n/)
    addset(newf)
    f2 = File.open('result/dict/custom_word.wd','w+')
    count = 0
    @wd_pool.each{|k,v|
      f2.write("#{k} #{v} n\n")
      count += 1
    }
    @logger.info("[#{wd_date}] after computation custom_word.wd had #{count} words now.")
    @logger.info("[#{wd_date}] increased #{count.to_i - wleng.to_i} words today.")
  else
    @logger.warn("not found result/newwd/#{wd_date}.wd. - skip it")
  end
else
  @logger.error("execution failed - taskdate: #{wd_date}")
end
