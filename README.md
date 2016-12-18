# hexa
**Introduction**

A **fingerprint enabled Payment** Gateway System that can be implemented in small communities (eg: College campus). This eliminates the need to use traditional money for carrying out transactions inside the community.

The members of this community can register for an e-wallet and spend their money through the POS system provided by us at the shops using their fingerprints. The users can add money to their e-wallet through the web portal or the App provided by us.

**Background**

The problems faced are:

- They need to carry cash or card to make payments in the shops present inside their campus.
- They needed to give exact change to the shop keeper which is always a hassle, which in turn increases the time taken for the transaction.
- They needed to make a frequent visit to the ATM to withdraw cash.

**Our Solution**

Our idea will make the students life easier by decreasing the need to carry cash or card to make payments in the shops present inside their campus. It will eliminate the need to give exact change by shop keeper which is always a hassle, also reduces the time of transaction.

The online recharge facility which we provide can be used to transfer money directly to their e-wallet which in turn reduces the No. of trips to the ATMs.

Our project uses technology to make everyday payments at local stores easy and convenient for the customers as well as shopkeepers.

The fingerprint happens to be unique for every person and it is always at their fingertips, so our project leverages this as an identification to make payments. This completely eliminates the need to carry around any kind of traditional currency or cards.

**Project**

The Project enable cash less payment in small community spaces (e.g. College campus). All the shops inside the community will house a Point of Sales System each to carry out transactions. Every user has an e-account which is linked to his mobile number (used as account number) and his fingerprint.

The POS (Point of Sales) systems has Four features:

- Registration
- Payment
- Recharge
- Mini-Statement

And a web application to check the statement and also transfer funds between peers.

Registration: To register a new customer into the system the vendor pushes the registration button to initiate the process which is followed by entering mobile number and then scanning any two fingers of the customer. The displays and buzzers engages and guides the customers through the process.

Payment / Recharger: Both follows same workflow. The vendor enters the amount using the numeric keypad which will be displayed on the displays the customer can confirm and acknowledge the payment/recharge by placing the finger on the scanner which will proceed and displays the status (success /failure) of the process.

Mini-Statement: If the customer wishes to check details of the last three transaction they can put the finger on the scanner the mini statement will appear for 5 sec.

Web Application Features:

- Recharge
  - Using this feature you can add money to your wallet
  - To facilitate secure online recharge through Net banking / Debit card we are using a third-party payment gateway - &quot;RazorPay&quot;.
- Fund transfer between peers
  - This feature enables a user to transfer funds to other users of the wallet system.
- Check balance
  - The feature allows a user to check the balance in the account.
- View complete account statement
  - The user can view the complete transaction history of the wallet account.
  - An option to download the account statement in excel format is also provided.
- Edit profile
  - Using this feature the user can modify his account details like follows:
    - Profile picture
    - Full name
    - Contact email address
  - The user cannot modify his mobile numbers using this feature because it is linked to his unique fingerprint.
  - Though this feature can be added in the future using a prescribed method.

**Technical Details**

**Sensor&#39;s Used:**

- Fingerprint Scanner
  - Manufacturer : SecuGen
  - Model : SDA04PX
  - Features : Inbuilt processor( comparison takes less than 0.1 sec), 10,000 Fingerprints can be stored , Fingerprint database can be transferred, UART.

- Real Time Clock
  - To Track down current time.

- Display
  - JHD12864 -Graphic LCD 128x64(2 displays are used)

- Buzzer
  - Used for indication of task completion

**Platform Used:**

- Hardware : Raspberry Pi Model B+
- Programming Language : Python
- Database : SQLite

**Construction:**

The POS System has 2 GLCD displays one facing customer side and the other facing vendor side.

There are four push buttons which is configured to initiate &quot;Registration mode&quot;, &quot;Payment mode&quot;, &quot;Recharge mode&quot; and one as &quot;back button&quot;.

There is a numeric key pad attached to the Raspberry Pi through one of USB port which is used for billing.

The fingerprint scanner has an auto detect feature which is used for showing the mini statement (i.e. details like Date, Time, Venue, Recharge/Payment, Amount) of the last three transactions.

After every successful task the buzzer produces a sound as a feedback.
