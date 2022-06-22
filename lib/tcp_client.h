// -*- c++ -*-
// Copyright (c) Microsoft Corporation.
// Licensed under the GNU General Public License v3.0 or later.
// See License.txt in the project root for license information.

#ifndef INCLUDED_AZURE_SOFTWARE_RADIO_TCP_CLIENT_H
#define INCLUDED_AZURE_SOFTWARE_RADIO_TCP_CLIENT_H

#include <string>
#include <netinet/in.h>


namespace gr {
namespace azure_software_radio {

class tcp_client
{
    public:

        tcp_client(std::string ip_addr, uint32_t port);
        ~tcp_client();

        bool connect();
        bool is_connected();
        int send(int8_t* buf, int lent);

    private:

        void create_socket();

        int d_socket;
        struct sockaddr_in d_servaddr;
};

} // namespace azure_software_radio
} // namespace gr

#endif /* INCLUDED_AZURE_SOFTWARE_RADIO_TCP_CLIENT_H */