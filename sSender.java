package scctvServer;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

import java.util.HashMap;
import java.util.Iterator;

public class sSender extends Thread {
	String name;
	Socket socket;
	DataOutputStream out;
	
	sSender(Socket socket){
		this.socket = socket;
		try{
			out=new DataOutputStream(socket.getOutputStream());
			name = "[" + socket.getInetAddress() + ":" + socket.getPort()
					+ "]";
		}catch(Exception e){
			e.printStackTrace();		}
	}
	
	@Override
	public void run(){
		Scanner scanner = new Scanner(System.in);
		while(out!=null){
			try{
				out.writeUTF(name + scanner.nextLine());
			}catch(IOException e){
				e.printStackTrace();
			}
		}
	}
}
