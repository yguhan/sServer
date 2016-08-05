package scctvServer;

import java.io.DataInput;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;

import java.util.HashMap;
import java.util.Iterator;


public class sReceiver extends Thread {
	
	Socket socket;
	DataInputStream in;
	//why ? ?
	sReceiver(Socket socket){
		this.socket = socket;
		try{
			in = new DataInputStream(socket.getInputStream());
		}catch(IOException e){
			e.printStackTrace();
		}
	}
	
	@Override
	public void run(){
		while(in!= null){
			try{
				System.out.println(in.readUTF());
			}catch(IOException e){
				e.printStackTrace();
			}
		}
	}
}
