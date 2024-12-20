function abs(valor) {
  if (valor < 0) {
    return -valor
  } else {
    return valor
  }
}

BEGIN {
  alpha = 0.125
  beta = 0.25
  k = 4 

  if (ARGC > 3) {
    alpha = ARGV[3]
  }
  if (ARGC > 4) {
    beta = ARGV[4]
  }

  nombre_archivo = ARGV[1]
  nombre_salida = ARGV[2]

  print "SampleRTT,EstimatedRTT,DevRTT,TimeoutInterval" > nombre_salida
}

{
  gsub(/\r/, "", $1)
  
  sample_rtt = $1
  if (NR == 1) {
    estimated_rtt = sample_rtt
    dev_rtt = sample_rtt / 2
  } else {
    estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
    dev_rtt = (1 - beta) * dev_rtt + beta * abs(sample_rtt - estimated_rtt)
  }
  timeout_interval = estimated_rtt + k * dev_rtt
  print sample_rtt "," estimated_rtt "," dev_rtt "," timeout_interval >> nombre_salida
}