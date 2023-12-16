Feature: deleting an item from the fridge
  In order to avoid cluttering my dashboard and views with items no longer in the fridge,
  As a user,
  I want to be able to delete items from the dashboard
  So that the dashboard better represents what I have in the fridge at any time.

  Scenario Outline: click the delete button
     Given that "<item>" is on the dashboard
     When I delete the "<item>" from the dashboard
     Then "<item>" will no longer appear in the dashboard

   Examples:
    | item          |
    | rotten eggs   |
    | milk          |
