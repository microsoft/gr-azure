// -*- c++ -*-
// Copyright (c) Microsoft Corporation.
// Licensed under the GNU General Public License v3.0 or later.
// See License.txt in the project root for license information.

#ifndef INCLUDED_AZURE_SOFTWARE_RADIO_TCP_SERVER_H
#define INCLUDED_AZURE_SOFTWARE_RADIO_TCP_SERVER_H

#include <gnuradio/logger.h>
#include <string>
#include <netinet/in.h>


namespace gr {
namespace azure_software_radio {

class tcp_server
{
    public:

        tcp_server(std::string ip_addr, uint32_t port);
        ~tcp_server();

        bool is_client_connected();
        int read(int8_t* buf, int len);

        int num_bytes_available();


    private:

        void check_for_incoming_conn(int timeout_in_ms=100);
        void reset_client_conn();

        bool is_data_available(int timeout_in_ms=100);

        int d_listener;
        int d_client;
        struct sockaddr_in d_servaddr;
        gr::logger d_logger;
};

} // namespace azure_software_radio
} // namespace gr

#endif /* INCLUDED_AZURE_SOFTWARE_RADIO_TCP_SERVER_H */