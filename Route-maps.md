### Route maps
Route maps are one of the most versatile and powerful tools in Cisco networking. They allow you to define policies for routing, filtering, and modifying traffic behavior. Route maps can be used in a variety of scenarios, ranging from controlling routing protocols to implementing advanced traffic engineering. Below is a detailed list of **use cases for route maps** along with explanations and examples.

---

### **1. Controlling BGP Route Advertisement**
Route maps are extensively used in Border Gateway Protocol (BGP) to control which routes are advertised or received.

#### **Use Case: Filtering Routes**
You can use route maps to filter specific prefixes or attributes before advertising them to BGP peers.

- **Example**: Advertise only specific prefixes to a BGP neighbor.
```bash
ip prefix-list OUTBOUND permit 192.168.1.0/24
ip prefix-list OUTBOUND permit 192.168.2.0/24

route-map FILTER-OUT permit 10
 match ip address prefix-list OUTBOUND

router bgp 65001
 neighbor 10.0.0.2 route-map FILTER-OUT out
```

---

### **2. Modifying BGP Attributes**
Route maps can modify BGP attributes such as Local Preference, MED (Multi-Exit Discriminator), AS Path, and Communities.

#### **Use Case: Setting Local Preference**
Increase the preference for specific routes to influence traffic flow.

- **Example**: Set Local Preference for certain routes.
```bash
ip prefix-list HIGH-PRIORITY permit 192.168.1.0/24

route-map SET-LOCAL-PREF permit 10
 match ip address prefix-list HIGH-PRIORITY
 set local-preference 200

router bgp 65001
 neighbor 10.0.0.2 route-map SET-LOCAL-PREF in
```

#### **Use Case: Setting MED**
Modify the MED value to influence inbound traffic from external peers.

- **Example**: Set MED for outbound routes.
```bash
route-map SET-MED permit 10
 set metric 100

router bgp 65001
 neighbor 10.0.0.2 route-map SET-MED out
```

---

### **3. Policy-Based Routing (PBR)**
Route maps are used in Policy-Based Routing (PBR) to override the default routing behavior based on source IP, destination IP, protocol, or other criteria.

#### **Use Case: Redirect Traffic Based on Source IP**
Redirect traffic from a specific source IP to a different next-hop.

- **Example**: Redirect traffic from `192.168.1.0/24` to a specific next-hop.
```bash
access-list 10 permit 192.168.1.0 0.0.0.255

route-map PBR-MAP permit 10
 match ip address 10
 set ip next-hop 10.0.0.1

interface GigabitEthernet0/1
 ip policy route-map PBR-MAP
```

---

### **4. Redistribution Control**
When redistributing routes between routing protocols (e.g., OSPF to BGP or EIGRP to OSPF), route maps can control which routes are redistributed and how they are modified.

#### **Use Case: Redistribute Only Specific Routes**
Redistribute only certain routes while denying others.

- **Example**: Redistribute only specific prefixes from OSPF to BGP.
```bash
ip prefix-list REDISTRIBUTE permit 192.168.1.0/24
ip prefix-list REDISTRIBUTE permit 192.168.2.0/24

route-map CONTROL-REDIST permit 10
 match ip address prefix-list REDISTRIBUTE

router ospf 1
 redistribute bgp 65001 route-map CONTROL-REDIST
```

---

### **5. Traffic Engineering**
Route maps can be used to manipulate routing decisions for traffic engineering purposes.

#### **Use Case: Modify Next-Hop**
Change the next-hop for specific routes to influence traffic paths.

- **Example**: Modify the next-hop for routes matching a prefix list.
```bash
ip prefix-list MODIFY-NEXT-HOP permit 192.168.1.0/24

route-map MODIFY-NEXT-HOP permit 10
 match ip address prefix-list MODIFY-NEXT-HOP
 set ip next-hop 10.0.0.1
```

---

### **6. Implementing QoS Policies**
Route maps can classify traffic for Quality of Service (QoS) purposes by matching specific criteria.

#### **Use Case: Classify Traffic for QoS**
Classify traffic based on source/destination IPs or protocols.

- **Example**: Match traffic from a specific subnet for QoS marking.
```bash
access-list 10 permit 192.168.1.0 0.0.0.255

route-map QOS-MAP permit 10
 match ip address 10
 set dscp af41

class-map QOS-CLASS
 match route-map QOS-MAP

policy-map QOS-POLICY
 class QOS-CLASS
  set dscp af41
```

---

### **7. BGP Community Manipulation**
Route maps are commonly used to tag routes with BGP communities for easier management and filtering.

#### **Use Case: Set Communities**
Tag routes with a specific BGP community.

- **Example**: Add a community tag to specific routes.
```bash
ip prefix-list TAG-COMMUNITY permit 192.168.1.0/24

route-map SET-COMMUNITY permit 10
 match ip address prefix-list TAG-COMMUNITY
 set community 65001:100

router bgp 65001
 neighbor 10.0.0.2 route-map SET-COMMUNITY out
```

---

### **8. Conditional Default Routing**
Route maps can be used to conditionally inject a default route into a routing protocol.

#### **Use Case: Inject Default Route**
Inject a default route into OSPF if certain conditions are met.

- **Example**: Inject a default route into OSPF when a specific route exists.
```bash
ip route 192.168.1.0 255.255.255.0 Null0

route-map DEFAULT-ROUTE permit 10
 match ip address 1

router ospf 1
 default-information originate route-map DEFAULT-ROUTE
```

---

### **9. Summarization**
Route maps can be used in conjunction with summarization to aggregate routes and apply policies.

#### **Use Case: Aggregate Routes**
Summarize routes and apply a route map to control advertisement.

- **Example**: Summarize routes and advertise the summary.
```bash
route-map SUMMARIZE permit 10
 set ip next-hop 10.0.0.1

router bgp 65001
 aggregate-address 192.168.0.0 255.255.0.0 summary-only
 neighbor 10.0.0.2 route-map SUMMARIZE out
```

---

### **10. Security and Access Control**
Route maps can be used to enforce security policies by filtering or modifying routes.

#### **Use Case: Block Unwanted Routes**
Block unwanted routes from being learned or advertised.

- **Example**: Deny specific routes from a BGP neighbor.
```bash
ip prefix-list BLOCK deny 10.10.0.0/16
ip prefix-list BLOCK permit 0.0.0.0/0 le 32

route-map BLOCK-ROUTES permit 10
 match ip address prefix-list BLOCK

router bgp 65001
 neighbor 10.0.0.2 route-map BLOCK-ROUTES in
```

---

### **11. Conditional Route Injection**
Route maps can be used to inject routes into a routing protocol based on specific conditions.

#### **Use Case: Inject Static Routes Dynamically**
Inject static routes into OSPF dynamically based on route map conditions.

- **Example**: Inject static routes into OSPF if they meet certain criteria.
```bash
ip route 192.168.1.0 255.255.255.0 Null0

route-map INJECT-STATIC permit 10
 match ip address 1

router ospf 1
 redistribute static route-map INJECT-STATIC
```

---

### **Summary Table of Use Cases**

| **Use Case**                     | **Description**                                                                 |
|----------------------------------|---------------------------------------------------------------------------------|
| BGP Route Filtering             | Filter routes advertised or received in BGP.                                    |
| BGP Attribute Modification       | Modify Local Preference, MED, AS Path, or Communities.                          |
| Policy-Based Routing (PBR)      | Override default routing based on source/destination IPs or other criteria.     |
| Redistribution Control          | Control which routes are redistributed between routing protocols.              |
| Traffic Engineering             | Modify next-hop or routing decisions for traffic engineering.                   |
| QoS Classification              | Classify traffic for Quality of Service (QoS) policies.                         |
| BGP Community Manipulation      | Tag routes with BGP communities for easier management and filtering.            |
| Conditional Default Routing     | Conditionally inject default routes into a routing protocol.                    |
| Summarization                   | Aggregate routes and apply policies during summarization.                       |
| Security and Access Control     | Block or filter unwanted routes for security purposes.                          |
| Conditional Route Injection     | Inject routes into a routing protocol based on specific conditions.             |

---

### **Conclusion**
Route maps are incredibly flexible and can be applied to a wide range of networking tasks. From controlling BGP behavior to implementing advanced traffic engineering and security policies, route maps provide granular control over routing and traffic behavior. Understanding their syntax and capabilities is essential for network engineers working in complex environments.
