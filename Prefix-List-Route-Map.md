### **Cisco Prefix-List, Route-Map, and Usage Cases**

In Cisco networking, **Prefix Lists** and **Route Maps** are powerful tools used to control and manipulate routing information. They are commonly used in conjunction with routing protocols (e.g., BGP, OSPF, EIGRP) or policy-based routing (PBR). Below is an explanation of each concept, their configuration syntax, and common use cases.

---

### **1. Prefix List**
A **prefix list** is used to filter IP prefixes (networks) based on their prefix length and address. It is more flexible and precise than access control lists (ACLs) for routing purposes.

#### **Syntax**
```bash
ip prefix-list <name> [seq <sequence-number>] <permit|deny> <network>/<prefix-length> [ge <min-prefix-length>] [le <max-prefix-length>]
```

- `<name>`: The name of the prefix list.
- `seq`: Optional sequence number to define the order of entries.
- `permit|deny`: Whether to allow or block the prefix.
- `<network>/<prefix-length>`: The network address and its prefix length.
- `ge`: Greater than or equal to a specific prefix length.
- `le`: Less than or equal to a specific prefix length.

#### **Example**
Allow only `/24` networks within `192.168.0.0/16`:
```bash
ip prefix-list FILTER permit 192.168.0.0/16 ge 24 le 24
```

This allows prefixes like `192.168.1.0/24`, `192.168.2.0/24`, but denies `192.168.0.0/16` or `192.168.1.0/25`.

---

### **2. Route Map**
A **route map** is a policy tool that allows you to match and set attributes for routes. It is often used with routing protocols (e.g., BGP) or PBR to modify route behavior.

#### **Syntax**
```bash
route-map <name> <permit|deny> [<sequence-number>]
 match <criteria>
 set <action>
```

- `<name>`: The name of the route map.
- `permit|deny`: Whether to allow or block the route.
- `match`: Specifies the criteria to match (e.g., prefix list, AS path, metric).
- `set`: Specifies the action to take if the route matches (e.g., change next-hop, metric, community).

#### **Example**
Modify the next-hop for routes matching a prefix list:
```bash
route-map MODIFY-NEXT-HOP permit 10
 match ip address prefix-list FILTER
 set ip next-hop 10.0.0.1
```

This changes the next-hop to `10.0.0.1` for routes matching the prefix list `FILTER`.

---

### **3. Common Use Cases**

#### **3.1 Filtering Routes in BGP**
You can use prefix lists and route maps to filter routes advertised or received in BGP.

- **Filter Advertised Routes**:
  Only advertise specific prefixes to a BGP peer.
  ```bash
  ip prefix-list OUTBOUND permit 192.168.1.0/24
  ip prefix-list OUTBOUND permit 192.168.2.0/24

  route-map FILTER-OUT permit 10
   match ip address prefix-list OUTBOUND

  router bgp 65001
   neighbor 10.0.0.2 route-map FILTER-OUT out
  ```

- **Filter Received Routes**:
  Block unwanted routes from a BGP peer.
  ```bash
  ip prefix-list INBOUND deny 10.10.0.0/16
  ip prefix-list INBOUND permit 0.0.0.0/0 le 32

  route-map FILTER-IN permit 10
   match ip address prefix-list INBOUND

  router bgp 65001
   neighbor 10.0.0.2 route-map FILTER-IN in
  ```

---

#### **3.2 Modifying BGP Attributes**
You can use route maps to modify BGP attributes such as Local Preference, MED, or Communities.

- **Set Local Preference**:
  Increase the preference for specific routes.
  ```bash
  ip prefix-list HIGH-PRIORITY permit 192.168.1.0/24

  route-map SET-LOCAL-PREF permit 10
   match ip address prefix-list HIGH-PRIORITY
   set local-preference 200

  router bgp 65001
   neighbor 10.0.0.2 route-map SET-LOCAL-PREF in
  ```

- **Set Community**:
  Tag routes with a specific BGP community.
  ```bash
  ip prefix-list TAG-COMMUNITY permit 192.168.1.0/24

  route-map SET-COMMUNITY permit 10
   match ip address prefix-list TAG-COMMUNITY
   set community 65001:100

  router bgp 65001
   neighbor 10.0.0.2 route-map SET-COMMUNITY out
  ```

---

#### **3.3 Policy-Based Routing (PBR)**
Route maps can be used for policy-based routing to override the default routing behavior.

- **Redirect Traffic Based on Source IP**:
  Redirect traffic from a specific source IP to a different next-hop.
  ```bash
  access-list 10 permit 192.168.1.0 0.0.0.255

  route-map PBR-MAP permit 10
   match ip address 10
   set ip next-hop 10.0.0.1

  interface GigabitEthernet0/1
   ip policy route-map PBR-MAP
  ```

---

#### **3.4 Redistribution Control**
When redistributing routes between routing protocols (e.g., OSPF to BGP), you can use prefix lists and route maps to control which routes are redistributed.

- **Redistribute Only Specific Routes**:
  ```bash
  ip prefix-list REDISTRIBUTE permit 192.168.1.0/24
  ip prefix-list REDISTRIBUTE permit 192.168.2.0/24

  route-map CONTROL-REDIST permit 10
   match ip address prefix-list REDISTRIBUTE

  router ospf 1
   redistribute bgp 65001 route-map CONTROL-REDIST
  ```

---

#### **3.5 Summarization**
You can summarize routes using prefix lists and route maps to reduce the size of the routing table.

- **Summarize Routes**:
  ```bash
  ip prefix-list SUMMARY permit 192.168.0.0/16 ge 24 le 24

  route-map SUMMARIZE permit 10
   match ip address prefix-list SUMMARY
   set ip next-hop 10.0.0.1

  router bgp 65001
   aggregate-address 192.168.0.0 255.255.0.0 summary-only
  ```

---

### **4. Summary Table of Use Cases**

| **Use Case**                   | **Prefix List**                                                                 | **Route Map**                                                                 |
|--------------------------------|--------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| Filter BGP Routes              | Match specific prefixes to allow/deny.                                         | Apply prefix list to filter inbound/outbound BGP routes.                     |
| Modify BGP Attributes          | Match prefixes for attribute changes.                                          | Set Local Preference, MED, or Community values for matched routes.           |
| Policy-Based Routing (PBR)     | Match source/destination IPs for traffic redirection.                          | Redirect traffic to a specific next-hop based on ACL/prefix list matches.    |
| Redistribution Control         | Match prefixes to control redistribution between protocols.                    | Allow/deny specific routes during redistribution.                            |
| Summarization                  | Match prefixes for summarization.                                              | Aggregate routes and advertise summarized prefixes.                          |

---

### **Conclusion**
Prefix lists and route maps are essential tools for controlling and manipulating routing behavior in Cisco networks. By combining them effectively, you can achieve granular control over route filtering, attribute modification, and policy-based routing. These tools are particularly valuable in complex environments like BGP peering, multi-protocol redistribution, and advanced traffic engineering. If you need further clarification or examples for a specific scenario, feel free to ask!
