Feature: deleting an item from the fridge
  Scenario: call delete endpoint
     Given we have an item X on the dashboard
      When we call the delete endpoint on item X
      Then item X no longer appears in the dashboard
