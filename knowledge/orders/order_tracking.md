# Order Tracking Policy

## Order Status

Customers can request the current status of an order by providing their Order ID.

The support system should use the order information available in the company order database to determine the current order status.

## Available Order Statuses

An order may have one of the following statuses:

- pending
- approved
- processing
- shipped
- delivered
- cancelled

The support agent must not invent an order status.

## Tracking Information

If the database contains shipping or delivery information, the support agent may provide the available information to the customer.

The agent must distinguish between:

- confirmed delivery information
- estimated delivery information

An estimated delivery date must not be presented as a guaranteed delivery date.

## Missing Order Information

If the Order ID is missing, ask the customer for the Order ID.

If the Order ID cannot be found in the company database, inform the customer that the order could not be located and request that they verify the Order ID.

## Delivery Delay

If the current order information indicates that the order has not arrived by the estimated delivery date, the case may require further investigation according to the delayed delivery policy.

## Important Rule

The support agent must never invent:

- an Order ID
- a delivery date
- a shipping status
- tracking information
- a carrier