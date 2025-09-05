# Domain Description

A retailer purchases stock in **batches** from manufacturers and stores in the warehouse. Using our ecommerce website customers then are able to place **orders** for available products, until the batch runs out and the product listing changes status to "Out of Stock". Current system presents information based only on stock physically available in the warehouse. Our goal and improvement is to treat batches in transit from the manufacturer as real stock and part of the inventory and use their estimated arrival time to show extended lead times to customers, and thus reduce "Out of Stock" listings on the website and hopefully sell more product.


## Order

Represents goods purchased by a customer and is identified by **order reference** and comprises multiple **order lines**.

### Order Line

Has two properties: **SKU** and a **quantity**. E.g.:

- **13** units of **COZY-BLANKET**
- **1** unit of **CUSHY-SOFA**

## Batch

Represents stock ordered by purchasing department. Has a unique ID called **reference**, a **SKU** and a **quantity**. Additionally, batches that are currently shipping have an **ETA**. This distinguishes them from batches that are already in the warehouse.

## Allocation
- We cannot allocate order to a batch if the available quantity is less than the required quantity of the order line
- We cannot allocate the same order line twice
- We want to prioritize allocating to warehouse stock, then to the earliest shipment batches.

