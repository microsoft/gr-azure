// -*- c++ -*-
// Copyright (c) Microsoft Corporation.
// Licensed under the GNU General Public License v3.0 or later.
// See License.txt in the project root for license information.

#ifndef INCLUDED_AZURE_SOFTWARE_RADIO_UDP_SOCKET_H
#define INCLUDED_AZURE_SOFTWARE_RADIO_UDP_SOCKET_H

#include <netinet/in.h>
#include <string>

namespace gr {
namespace azure_software_radio {

class udp_socket
{
    public:

        udp_socket(std::string ip_addr, uint32_t port, bool isServer, uint32_t socket_buffer_size=2000000);
        ~udp_socket();

        int read(int8_t* buf, int len);
        int send(int8_t* buf, int len);

    private:
        int d_socket;
        struct sockaddr_in d_servaddr;
};

} // namespace azure_software_radio
} // namespace gr

#endif /* INCLUDED_AZURE_SOFTWARE_RADIO_UDP_SOCKET_H */