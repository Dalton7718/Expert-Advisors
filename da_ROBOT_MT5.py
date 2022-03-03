//+------------------------------------------------------------------+
//|                                                  CatsAndDogs.mq5 |
//|                                           Copyright Dalton Tsima |
//|                                            tdalton7718@gmail.com |
//+------------------------------------------------------------------+
#property copyright "Copyright Dalton Tsima"
#property link      "tdalton7718@gmail.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh> // get other codes 

//-----------input variables
input double lotsize = 2.0;
input bool useStopLoss = true;
input int slippage = 3;
input int takeProfit = 10;

//--- service variables
CTrade myTradingControlPanel;
MqlRates PriceData[];

int OnInit()
  {
//--- data table for time series data
   ArraySetAsSeries(PriceData,true);
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//--- Collect the most current data
   double bidPrice = NormalizeDouble(SymbolInfoDouble(_Symbol,SYMBOL_BID),_Digits); // Getting the Bid Price
   double askPrice = NormalizeDouble(SymbolInfoDouble(_Symbol,SYMBOL_ASK),_Digits); // Getting the Ask Price
   
   Comment("The bid price of " + _Symbol + " is " + (string) bidPrice + "."); // Print some stuff
   Comment("The ask price of " + _Symbol + " is " + (string) askPrice + "."); // Print some stuff
   
   
//-----number of price data points useful in our robot
   int numberofPriceDataPoints = CopyRates(_Symbol,0,0,10, PriceData);
   double currentOpenPrice = PriceData[0].open;
  
   Comment("The current open is " + (string) currentOpenPrice);
   
   // create variables for our price data points
   
// check if we have open positions
   if (PositionSelect(_Symbol) == true) // we have an open position baba!
   {
   
   //----------------EXITS--------------------------------------------   
   //--- we exist short positions when bid == previous high
   //--when the current bar closes
  
   if ((PriceData[0].high - PriceData[0].low) > 0.35) // rule for exiting our short position //askPrice == PriceData[1].high ||
   //check how many positions we have
   if (PositionsTotal() <=2)
   {
   if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL) // if its a short position
   {
   CloseSells();
               } 
         }

//-----EXITING LONG POSITIONS-------------------
   if ((PriceData[0].high - PriceData[0].low) > 0.5) // rule for exiting long trades
   if (PositionsTotal() <=3)
   {
   if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY) // if its a buy position
          {
   CloseBuys();
            } 
         }
   }
   
//------------------------ENTRY RULES---------------------------------------------------------
//-----------------------SELL ENTRY RULES
  while (PriceData[1].close <= PriceData[0].low);
  {
  if (PositionSelect(_Symbol)== false) // checking if we have any open positions
  {
  if (PriceData[0].open)
  {
  myTradingControlPanel.Sell(2.0,NULL,bidPrice,(bidPrice+600.00*_Point), (bidPrice-500.000 * _Point), NULL);
  }
  if(myTradingControlPanel.ResultRetcode()==10008 || myTradingControlPanel.ResultRetcode()==10009) //Request is completed or order placed
       OpenOrders();
  
  }
//--------------------BUY ENTRY RULES-------------------------------------------------------------
   while ((PriceData[0].high - PriceData[0].low) > 0.38); // our entry rule for a buy
   {
   myTradingControlPanel.Buy(1.0,NULL,bidPrice,(bidPrice+3000.00*_Point), (bidPrice-500.000 * _Point), NULL);
   }
   OpenOrders();
   
      }
   }

//-------------FUNCTIONS------------------------------------------------------------------------------
//-------------CLOSE SELL POSITIONS-------------------------------------------------------------------
void CloseSells()
 {
 // count untill there are no positions left
   for (int i = PositionsTotal() -1 ; i >= 0 ; i--) // go through all ten positions
   {
      // get the ticket number for the current positions
      int ticket = PositionGetTicket(i);
      
      //Get the positions direction
      int PositionDirection = PositionGetInteger(POSITION_TYPE);
      
      //check if its a sell position we want
      if (PositionDirection==POSITION_TYPE_SELL)
      
      // close the current posistion
      myTradingControlPanel.PositionClose(ticket);
      
      } // end for loop
     
   } // end of function
   
//-------------------CLOSE BUYS-------------------------------------------------------------------------

void CloseBuys()
 
 {
 // count untill there are no positions left
   for (int j = PositionsTotal() -1 ; j >= 0 ; j--) // go through all ten positions
   {
      // get the ticket number for the current positions
      int ticket = PositionGetTicket(j);
      
      //Get the positions direction
      int PositionDirectionB = PositionGetInteger(POSITION_TYPE);
      
      //check if its a sell position we want
      if (PositionDirectionB==POSITION_TYPE_BUY)
      
      // close the current posistion
      myTradingControlPanel.PositionClose(ticket);
      
      } // end for loop
     
   } // end of function   
   
//-----------------------OPEN ORDERS FUNCTION-------------------------------------------
void OpenOrders()
{
if(myTradingControlPanel.ResultRetcode()==10008 || myTradingControlPanel.ResultRetcode()==10009) //Request is completed or order placed
            {
            Print("Entry rules: A Sell order has been successfully placed with Ticket#: ", myTradingControlPanel.ResultOrder());
            }
         else
            {
            Print("Entry rules: The Sell order request could not be completed. Error: ", GetLastError());
            ResetLastError();
            return;
            }
}
//----------------------------------------------------------------------------------------------