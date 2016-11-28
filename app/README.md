#Application


###server.py

This file contains the configurations of the web-server.


###demo.py

This file contains the views used to demo our product.

<ul>
<li> <b>webshop_demo</b> returns a demo page in where the DonateWise button has been integrated.</li>

<li> <b>create_donation</b> returns the view containing the form for making a donation. This view interact with the TransferWise APIs to get information about the source accounts (who is sending the money).</li>

<li> <b>process_donation</b> is responsible for processing the form and creating the transfer. To create a transfer, the following steps are executed:
    <ol type="1">
        <li> create quote </li>
        <li> create recipient account </li>
        <li> create transfer </li>
    </ol>
</li>
</ul>


###generate_button.py

This file contains the views responsible for generating the embedded code for button and the qr-code.


###static_files.py

This file contains the views responsible for serving static files (CSS, fonts, img and videos).


###services.py

This file contains general functions used in the project.