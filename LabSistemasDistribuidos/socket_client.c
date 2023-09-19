#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
void error( char *msg ) {
    perror(msg);
    exit(1);
}

int main( int argc, char *argv[] ) {

    int sockfd, portno, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;
    char buffer[256];

    if( argc < 3 ) {
        fprintf( stderr, "O comando deverá ter o formato: %s host porta\n", argv[0]);
        exit(1);
    }

    portno = atoi(argv[2]);

    sockfd = socket( AF_INET, SOCK_STREAM, 0 );
    
    if( sockfd < 0 ) {
        error("Erro ao abrir o socket");
    }
    server = gethostbyname(argv[1]);
    
    if( server == NULL ) {
        fprintf(stderr, "Erro ao encontrar o host\n" );
        exit(0);
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy( (char *) server->h_addr, (char *) &serv_addr.sin_addr.s_addr, server->h_length );
    serv_addr.sin_port = htons(portno);

    if( connect( sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0 ) {
        error("Erro ao conectar");
    }

    printf( "Entre com a mensagem: ");
    bzero(buffer, 256);
    fgets(buffer, 255, stdin);
    n = write( sockfd, buffer, strlen(buffer) );
    
    if( n < 0 ) {
        error("Erro ao escrever a mensagem no socket");
    }
    
    bzero( buffer, 256 );
    n = read( sockfd, buffer, 255 );
    
    if( n < 0 ) {
        error("Erro ao ler o socket");
    }

    printf("Mensagem recebida através do socket: %s\n", buffer );
    close(sockfd);
    
    return 0;
}
