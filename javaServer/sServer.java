package scctvServer;

// /home/yguhan/scctvServer/scctvServer/src/scctvServer
import java.io.IOException;
//import java.io.ObjectInputStream;
//import java.io.ObjectOutputStream;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.Date;

import scctvServer.sServer2.ServerReceiver;


public class sServer implements Runnable{
	
	@Override
	public void run(){
		try{
			System.out.println("Starting sCCTV Server");
			ServerSocket serverSocket = new ServerSocket(450);
			System.out.println("Listening port : 450");
			
			while(true){
				Socket socket = serverSocket.accept();
				ServerReceiver receiver = new ServerReceiver(socket);
	            receiver.start();
			}
			
		}catch(IOException e){
			e.printStackTrace();
		}
	}
	public static void main(String[] args){
		
		Thread sThread = new Thread(new sServer());
		sThread.start();
	}

   class ServerReceiver extends Thread {
        Socket socket;
        DataInputStream input;
        DataOutputStream output;
 
        public ServerReceiver(Socket socket) {
            this.socket = socket;
            System.out.println(getTime() + 
					"host: "+ socket.getInetAddress()+
					", port: "+socket.getPort());
        }
 
        @Override
        public void run() {
        	try{
        		while(true){
					BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
					if(in !=null){
						String str = in.readLine();
						System.out.println("s: Received: '" + str + "'");
					
						PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())));
						out.println("Server Received " +str);
					}
        		}
        	}catch(Exception e){
				e.printStackTrace();
			}finally{
				try {
					socket.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
        }
   }

	static String getTime(){
		SimpleDateFormat format = new SimpleDateFormat("yyyy-mm-dd [hh:mm:ss]");
		return format.format(new Date());
	}
}
