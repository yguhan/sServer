import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("postechserver@gmail.com", "wjswkghlfh")
 
msg = "YOUR MESSAGE!"
server.sendmail("postechserver@gmail.com", "yguhan@gmail.com", msg)
server.quit()
