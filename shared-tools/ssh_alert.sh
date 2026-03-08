#!/bin/bash

# Easy-to-understand version
TIME_WINDOW=${1:-5}          # How many minutes to check
ALERT_THRESHOLD=${2:-6}      # How many attempts trigger alarm

echo "Looking for SSH attacks in last $TIME_WINDOW minutes..."
echo "Will alert if more than $ALERT_THRESHOLD failed attempts from same IP"
echo ""

# Get SSH logs → find failures → extract IPs → count → alert
sudo journalctl SYSLOG_IDENTIFIER=sshd --since "$TIME_WINDOW minutes ago" \
  | grep -E "Failed password|Invalid user" \
  | awk '{print $(NF-3)}' \
  | sort | uniq -c | sort -nr \
  | awk -v threshold=$ALERT_THRESHOLD '
    {
      if ($1 >= threshold)
        print "🚨 ALERT: " $1 " failed attempts from " $2
      else
        print "✅ Normal: " $1 " attempts from " $2
    }'


#include<iostream>
using namespace std;

int n;
cin >> n;

int main(){

if (n%2 == 0){
  cout << n << " is even" << endl;
}
else{

  cout << n << " is odd" << endl;
}
}

#include<iostream>
using namespace std;

int a = 4;
int b = 8;
int c = 2;

int main(){

if (a>=b && a>=c){
   cout << a << "is largest" << endl;
}
else if(b>=a && b>=c){
   cout << b << "is largest" << endl;

}
else{
    cout << c << " is largest" << endl;
}
}

#include<iostream>
using namespace std;

int mark = 83;

int main(){

if (mark >= 90){
   cout << "A grade" << endl;
}
else if(mark >= 80 && mark < 90){
   cout << "B grade" << endl;
}
else if(mark>= 70 && mark < 80){
    cout << "C grade" << endl;
}
else if(mark >= 60 && mark < 70){
    cout << "D grade" << endl;
}
else{
    cout << "F grade" << endl;
}
