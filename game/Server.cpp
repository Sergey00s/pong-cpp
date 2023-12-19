#include "Server.h"
#include <cstring>


Server::Server()
{
	this->port = 2700;
	this->opt = 1;
	this->address.sin_family = AF_INET;
	this->address.sin_addr.s_addr = INADDR_ANY;
	this->address.sin_port = htons(this->port);
	this->server_fd = socket(AF_INET, SOCK_STREAM, 0);
	setsockopt(this->server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &this->opt, sizeof(this->opt));
	if (fcntl(this->server_fd, F_SETFL, O_NONBLOCK) < 0)
	{
		std::cout << "Failed to set socket to non-blocking" << std::endl;
		exit(EXIT_FAILURE);
	}
	if (this->server_fd == 0)
	{
		std::cout << "Failed to create socket" << std::endl;
		exit(EXIT_FAILURE);
	}
	if (bind(this->server_fd, (struct sockaddr *)&this->address, sizeof(this->address)) < 0)
	{
		std::cout << "Failed to bind socket" << std::endl;
		exit(EXIT_FAILURE);
	}
	if (listen(this->server_fd, 3) < 0)
	{
		std::cout << "Failed to listen" << std::endl;
		exit(EXIT_FAILURE);
	}
}

Server::Server(int port)
{
	this->port = port;
	this->opt = 1;
	this->address.sin_family = AF_INET;
	this->address.sin_addr.s_addr = INADDR_ANY;
	this->address.sin_port = htons(this->port);
	this->server_fd = socket(AF_INET, SOCK_STREAM, 0);
	setsockopt(this->server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &this->opt, sizeof(this->opt));
	if (fcntl(this->server_fd, F_SETFL, O_NONBLOCK) < 0)
	{
		std::cout << "Failed to set socket to non-blocking" << std::endl;
		exit(EXIT_FAILURE);
	}
	if (this->server_fd == 0)
	{
		std::cout << "Failed to create socket" << std::endl;
		exit(EXIT_FAILURE);
	}
	if (bind(this->server_fd, (struct sockaddr *)&this->address, sizeof(this->address)) < 0)
	{
		std::cout << "Failed to bind socket" << std::endl;
		exit(EXIT_FAILURE);
	}
	if (listen(this->server_fd, 3) < 0)
	{
		std::cout << "Failed to listen" << std::endl;
		exit(EXIT_FAILURE);
	}
}


Server::~Server()
{
	close(this->server_fd);
}

int &Server::getServerFd()
{
	return this->server_fd;
}

int &Server::getPort()
{
	return this->port;
}

int &Server::getOpt()
{
	return this->opt;
}

struct sockaddr_in &Server::getAddress()
{
	return this->address;
}


int Server::acceptConnection()
{
	int new_socket;
	int addrlen = sizeof(this->address);
	if ((new_socket = accept(this->server_fd, (struct sockaddr *)&this->address, (socklen_t *)&addrlen)) < 0)
	{
		std::cout << "Failed to accept connection" << std::endl;
		exit(EXIT_FAILURE);
	}
	return new_socket;
}


int Server::update()
{

	
	FD_ZERO(&this->readfds);
	FD_ZERO(&this->writefds);
	memset(&this->readfds, 0, sizeof(this->readfds));
	memset(&this->writefds, 0, sizeof(this->writefds));
	FD_SET(this->server_fd, &this->readfds);

	int max_sd = this->server_fd;

	for (int i = 0; i < this->clients.size(); i++)
	{
		int sd = this->clients[i];
		if (sd > 0)
		{
			FD_SET(sd, &this->readfds);
			FD_SET(sd, &this->writefds);
		}
		if (sd > max_sd)
			max_sd = sd;
	}

	struct timeval tv;
	tv.tv_sec = 0;
	tv.tv_usec = 0;
	int activity = select(max_sd + 1, &this->readfds, &this->writefds, NULL, &tv);
	if ((activity < 0) && (errno != EINTR))
	{
		std::cout << "Select error" << std::endl;
		exit(EXIT_FAILURE);
	}
	return activity;
}


int Server::recive_messages(std::vector<Message> &messages)
{
	int valread;
	char buffer[1024];
	for (int i = 0; i < this->clients.size(); i++)
	{
		int sd = this->clients[i];
		if (FD_ISSET(sd, &this->readfds))
		{
			if ((valread = read(sd, buffer, 1024)) == 0)
			{
				close(sd);
				this->clients.erase(this->clients.begin() + i);
			}
			else
			{
				Message message;
				message.client = sd;
				message.message = std::string(buffer);
				std::cout << "Message from client " << i << ": " << message.message << std::endl;
				message.address = i;
				messages.push_back(message);
			}
			memset(buffer, 0, 1024);
		}
	}
	return 0;
}



fd_set &Server::getReadfds()
{
	return this->readfds;
}


fd_set &Server::getWritefds()
{
	return this->writefds;
}

std::vector<int> &Server::getClients()
{
	return this->clients;
}