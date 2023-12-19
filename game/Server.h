#pragma once


#include <iostream>
#include <vector>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/select.h>

class Server
{
	int server_fd;
	int port;
	int opt;
	struct sockaddr_in address;
	std::vector<int> clients;

	class Message
	{
		public:
			int client;
			std::string message;
			int address;
	};

	public:
		std::vector<Message> messages;

	private:
		fd_set readfds;
		fd_set writefds;

	public:
		Server();
		Server(int port);
		~Server();
		int &getServerFd();
		fd_set &getReadfds();
		fd_set &getWritefds();
		std::vector<int> &getClients();
		int &getPort();
		int &getOpt();
		struct sockaddr_in &getAddress();
		int update();
		int acceptConnection();
		int recive_messages(std::vector<Message> &messages);

};