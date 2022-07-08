# AgentDan

## Synopsis

AgentDan is a custom **monitoring and alerting daemon** developed to monitor video packaging 
and streaming services for Encompass Digital Media services. Alerting is provide via an interface 
with **PagerDuty**. Dashboard is provide through integration with **Dashing**.

AgentDan currrently integrates with the following systems:

    1. Elemental Conductor
    2. Elemental Live

Coming Soon!
    1. Elemental Delta
    2. Envivio Halo
    3. MediaExcel Hero Live

## Code Example

    '''python
    #!/usr/bin/env python   
    """
    .. py:module:: AgentDan
    
    Example module implementing the Conductor module to check
    the status of all channels identified in Device.conf to be 
    monitored. The results will trigger or resolve PagerDuty 
    incidents.
    
    .. moduleauthor:: Doug Womack <dwomack@encompass.tv>
    """
    import time
    from AgentDan import config
    from AgentDan import Conductor
    def run():
        ec = Conductor()
        status, results = ec.checkStatus()
        try:
            if status == 200:
                config.log.info('{0}: {1}'.format(__name__, results))
        except Exception as e:
            config.log.error('ERROR): {0}'.format(e))
    
    if __name__ == '__main__':
        run()        
    '''

## Motivation

There currently is no method available to provide alerting and notification on any of the currently 
deployed streamers and packagers. The only available monitor capability is via MIBs through Solarwinds. 
These MIBs only provide a rudimentary level of monitoring mostly around the operating system resources. 
This is why AgentDan was developed.

## Installation

To deploy AgentDan, the following must be completed

    Prerequisites:
    - Request access to the AgentDan Git Repository by emailing dwomack@encompass.tv
    - A server running Linux and Python 2.7
    - pip installed - To get pip, run easy_install pip
    
    Steps:
    - Install git
        - yum install git or apt-get install git depending on distribution
    - Install xmltodict and requests via pip
        - pip install xmltodict requests
    - Clone repository and prepare files
        - Either sudo the following commands or su to root
        - cd /opt
        - git init
        - git clone git@git.assembla.com:agentdan.git
        - cd /opt/agentdan
        - chmod 755 *.py
        - chmod 755 AgentDan/*.py
    - Update /opt/agentdan/conf/Device.conf
        - under [Elemental Conductor] section
            - update with Conductor's IP address
            - provide list of IDs to monitor
    - At prompt, enter: python agentdan.py &
    
    At this point AgentDan is running. In /opt/agentdan/log, you can tail AgentDan.log
    to monitor progress.    

## API Reference

API Reference are available on http://phobos.encompass.tv/agentdan/

## Tests

All modules have doctest implemented.

## Contributors

Primary Developer: Doug Womack

## AgentDan - Terms and conditions

1. **Preamble:** This Agreement, signed on **date** (hereinafter: Effective Date) governs the relationship between Encompass Digital Media, a Business Entity, (hereinafter: Licensee) and **Licensor Name**, a duly registered company in whose principal place of business is **Licensor Address** (hereinafter: Licensor). This Agreement sets the terms, rights, restrictions and obligations on using AgentDan (hereinafter: The Software) created and owned by Licensor, as detailed herein <br />

2. **License Grant:** Licensor hereby grants Licensee a Personal, Non-assignable & non-transferable, Pepetual, Non-commercial, Without the rights to create derivative works, Non-exclusive license, all with accordance with the terms set forth and other legal restrictions set forth in 3rd party software used while running Software. <br />
 2.1 **Limited:** Licensee may use Software for the purpose of: <br />
  2.1.1 Running Software on Licensee’s Website[s] and Server[s]; <br />
  2.1.2 Allowing 3rd Parties to run Software on Licensee’s Website[s] and Server[s]; <br />
  2.1.3 Publishing Software’s output to Licensee and 3rd Parties; <br />
  2.1.4 Distribute verbatim copies of Software’s output (including compiled binaries); <br />
  2.1.5 Modify Software to suit Licensee’s needs and specifications. <br />
 2.2 This license is granted perpetually, as long as you do not materially breach it. <br />
 2.3 **Binary Restricted:** Licensee may sublicense Software as a part of a larger work containing more than Software, distributed solely in Object or Binary form under a personal, non-sublicensable, limited license. Such redistribution shall be limited to unlimited codebases. <br />
 2.4 **Non Assignable & Non-Transferable:** Licensee may not assign or transfer his rights and duties under this license. <br />
 2.5 **Non-Commercial:** Licensee may not use Software for commercial purposes. for the purpose of this license, commercial purposes means that a 3rd party has to pay in order to access Software or that the Website that runs Software is behind a paywall. <br />
 2.6 **With Attribution Requirements﻿:** <br />

3. **Term & Termination:** The Term of this license shall be until terminated. Licensor may terminate this Agreement, including Licensee’s license in the case where Licensee : <br />
 3.1 became insolvent or otherwise entered into any liquidation process; or <br />
 3.2 exported The Software to any jurisdiction where licensor may not enforce his rights under this agreements in; or <br />
 3.3 Licensee was in breach of any of this license's terms and conditions and such breach was not cured, immediately upon notification; or <br />
 3.4 Licensee in breach of any of the terms of clause 2 to this license; or <br />
 3.5 Licensee otherwise entered into any arrangement which caused Licensor to be unable to enforce his rights under this License. <br />

4. **Payment:** In consideration of the License granted under clause 2, Licensee shall pay Licensor a fee, via Credit-Card, PayPal or any other mean which Licensor may deem adequate. Failure to perform payment shall construe as material breach of this Agreement. <br />

5. **Upgrades, Updates and Fixes:** Licensor may provide Licensee, from time to time, with Upgrades, Updates or Fixes, as detailed herein and according to his sole discretion. Licensee hereby warrants to keep The Software up-to-date and install all relevant updates and fixes, and may, at his sole discretion, purchase upgrades, according to the rates set by Licensor. Licensor shall provide any update or Fix free of charge; however, nothing in this Agreement shall require Licensor to provide Updates or Fixes. <br />
 5.1 **Upgrades:** for the purpose of this license, an Upgrade shall be a material amendment in The Software, which contains new features and or major performance improvements and shall be marked as a new version number. For example, should Licensee purchase The Software under version 1.X.X, an upgrade shall commence under number 2.0.0. <br />
 5.2 **Updates:** for the purpose of this license, an update shall be a minor amendment in The Software, which may contain new features or minor improvements and shall be marked as a new sub-version number. For example, should Licensee purchase The Software under version 1.1.X, an upgrade shall commence under number 1.2.0. <br />
 5.3 **Fix:** for the purpose of this license, a fix shall be a minor amendment in The Software, intended to remove bugs or alter minor features which impair the The Software's functionality. A fix shall be marked as a new sub-sub-version number. For example, should Licensee purchase Software under version 1.1.1, an upgrade shall commence under number 1.1.2. <br />

6. **Support:** Software is provided under an AS-IS basis and without any support, updates or maintenance. Nothing in this Agreement shall require Licensor to provide Licensee with support or fixes to any bug, failure, mis-performance or other defect in The Software. <br />
 6.1 **Bug Notification:** Licensee may provide Licensor of details regarding any bug, defect or failure in The Software promptly and with no delay from such event; Licensee shall comply with Licensor's request for information regarding bugs, defects or failures and furnish him with information, screenshots and try to reproduce such bugs, defects or failures. <br />
 6.2 **Feature Request:** Licensee may request additional features in Software, provided, however, that (i) Licensee shall waive any claim or right in such feature should feature be developed by Licensor; (ii) Licensee shall be prohibited from developing the feature, or disclose such feature request, or feature, to any 3rd party directly competing with Licensor or any 3rd party which may be, following the development of such feature, in direct competition with Licensor; (iii) Licensee warrants that feature does not infringe any 3rd party patent, trademark, trade-secret or any other intellectual property right; and (iv) Licensee developed, envisioned or created the feature solely by himself. <br />

7. **Liability:**  To the extent permitted under Law, The Software is provided under an AS-IS basis. Licensor shall never, and without any limit, be liable for any damage, cost, expense or any other payment incurred by Licensee as a result of Software’s actions, failure, bugs and/or any other interaction between The Software  and Licensee’s end-equipment, computers, other software or any 3rd party, end-equipment, computer or services.  Moreover, Licensor shall never be liable for any defect in source code written by Licensee when relying on The Software or using The Software’s source code. <br />

8. **Warranty:** <br />
 8.1 **Intellectual Property:** Licensor hereby warrants that The Software does not violate or infringe any 3rd party claims in regards to intellectual property, patents and/or trademarks and that to the best of its knowledge no legal action has been taken against it for any infringement or violation of any 3rd party intellectual property rights. <br />
 8.2 **No-Warranty:** The Software is provided without any warranty; Licensor hereby disclaims any warranty that The Software shall be error free, without defects or code which may cause damage to Licensee’s computers or to Licensee, and that Software shall be functional. Licensee shall be solely liable to any damage, defect or loss incurred as a result of operating software and undertake the risks contained in running The Software on License’s Server[s] and Website[s]. <br />
 8.3 **Prior Inspection:** Licensee hereby states that he inspected The Software thoroughly and found it satisfactory and adequate to his needs, that it does not interfere with his regular operation and that it does meet the standards and scope of his computer systems and architecture. Licensee found that The Software interacts with his development, website and server environment and that it does not infringe any of End User License Agreement of any software Licensee may use in performing his services. Licensee hereby waives any claims regarding The Software's incompatibility, performance, results and features, and warrants that he inspected the The Software. <br />

9. **No Refunds:** Licensee warrants that he inspected The Software according to clause 7(c) and that it is adequate to his needs. Accordingly, as The Software is intangible goods, Licensee shall not be, ever, entitled to any refund, rebate, compensation or restitution for any reason whatsoever, even if The Software contains material flaws. <br />

10. **Indemnification:** Licensee hereby warrants to hold Licensor harmless and indemnify Licensor for any lawsuit brought against it in regards to Licensee’s use of The Software in means that violate, breach or otherwise circumvent this license, Licensor's intellectual property rights or Licensor's title in The Software. Licensor shall promptly notify Licensee in case of such legal action and request Licensee’s consent prior to any settlement in relation to such lawsuit or claim. <br />

11. **Governing Law, Jurisdiction:** Licensee hereby agrees not to initiate class-action lawsuits against Licensor in relation to this license and to compensate Licensor for any legal fees, cost or attorney fees should any claim brought by Licensee against Licensor be denied, in part or in full. <br />
