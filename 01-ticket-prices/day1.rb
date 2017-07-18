
$destination_values = {'Almaty' => 2.0, 'Brorfelde' => 0.9, 'Estacada' => 0.4, 
  'Jayuya' => 0.6, 'Karlukovo' => 2.2, 'Morgantown' => 2.9,'Nordkapp' => 1.5, 
  'Nullarbor' => 2.2, 'Puente-Laguna-Garzonkuala-Penyu' => 0.4, 'Uzupis' => 0.9}
$destination_values.default = 1.0

holidays = File.readlines('01-holidays.txt').map {|l| l.chomp.split}

def affordable_holidays(hs)
  hs.select {|h| h[1].to_i <= 1200}
end

def value(holiday)
  $destination_values[holiday[2]] * holiday[3].to_f / holiday[1].to_i 
end

part1 = affordable_holidays(holidays).length
part2 = affordable_holidays(holidays).max_by {|h| value h}.first

puts "Part 1: #{part1}\nPart 2: #{part2}"
