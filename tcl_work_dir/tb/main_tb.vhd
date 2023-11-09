--------------------------------------------------------------------------------------
-- Company Name: Department of Computer Science & Engineering / University of Ioannina 

-- Engineer: Georgios Papatheodorou

-- Module: TEST BENCH FILE

-- Module Name: main_tb

-- Revisions:
-- 
-- Additional Comments: 
--
--------------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use std.textio.all;
use ieee.std_logic_textio.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;




entity main_tb is
end main_tb;

architecture tb of main_tb is

    component main
        port (
			  IN_A 	 		: in  STD_LOGIC_VECTOR (7 downto 0);  --MULTIPLICAND
           IN_B 	 		: in  STD_LOGIC_VECTOR (7 downto 0);  --MULTIPLIER
			  IN_WR			: in 	STD_LOGIC;							  --INPUT REGISTER WRITE ENABLE
			  IN_RST			: in 	STD_LOGIC;							  --INPUT REGISTER RESET
			  CLK				: in 	STD_LOGIC;							  --CLOCK
           OUTPUT_A		: out STD_LOGIC_VECTOR (14 downto 0); --OUTPUT 1st line
			  OUTPUT_B		: out STD_LOGIC_VECTOR (14 downto 0); --OUTPUT 2nd line
			  OUT_WR			: in 	STD_LOGIC;							  --OUTPUT REGISTER WRITE ENABLE
			  OUT_RST		: in 	STD_LOGIC							  --OUTPUT REGISTER RESET
			  );							 
				
	end component;

	 
--INPUTS
    signal IN_A   : std_logic_vector (7 downto 0);
    signal IN_B   : std_logic_vector (7 downto 0);
	 signal IN_WR  : std_logic := '1';
	 signal IN_RST : std_logic := '0';
	 signal CLK 	: std_ulogic;
	 signal OUT_WR	: std_logic := '1';
	 signal OUT_RST: std_logic := '0';
--	 signal k 		: integer;
--	 signal m 		: integer;
	
	----------------------------------
	
--OUTPUTS
    signal OUTPUT_A : std_logic_vector (14 downto 0);
	 signal OUTPUT_B : std_logic_vector (14 downto 0);

	 ---------------------------------
-- COUNTER	 
	 signal countB : unsigned(7 downto 0) := "00000000"; 
	 signal countA : unsigned(7 downto 0) := "00000000";
 
	 ---------------------------------

--INSTANTIATE DEVICE UNDER TEST (DUT)
  

begin

    dut : main
	 
    port map (
					IN_A 		=> IN_A,
					IN_B 		=> IN_B,
					IN_WR		=> IN_WR,
					IN_RST	=> IN_RST,
					CLK		=>	CLK,
					OUT_WR	=> OUT_WR,
					OUT_RST	=> OUT_RST,
					OUTPUT_A	=> OUTPUT_A,
					OUTPUT_B => OUTPUT_B
				);
				
	  
	  
	  clock : process
	  
	  variable z 			: integer;
	  
	  variable outline 	: line;
	  
	  file outfile     	: text open write_mode is "C:\Users\papat\Desktop\8bit_Waters_AxC_Wallace_modular\Report8x8.txt";

	  constant num_cycles: integer := 65538;
	  
	  constant prd 		: time    := 3.119 ns; -- clock period 
	  
	 
	  begin

		
			for i in 1 to num_cycles loop
			
				CLK<= '0';
				wait for prd/2;
			    write (outline, ("0" & OUTPUT_A) + ("0" & OUTPUT_B), left, 16);
			    writeline(outfile, outline);

				
				CLK<= '1';
				wait for prd/2;
				
			end loop;
		wait; 

	end process;
	

-----------------------------------------------------------------------
    process(CLK)

	 begin
     
	  
		  if(rising_edge(CLK)) then				
				
				countB <= to_unsigned(to_integer(unsigned(countB)) + 1, 8);
					 
					 if(countB="11111111") then
					 
						countA <= to_unsigned(to_integer(unsigned(countA)) + 1, 8);		
					 
					 end if; 
		  
		  end if;
	
	 end process;
     
	  IN_B <= std_logic_vector(countB);
	  IN_A <= std_logic_vector(countA);

-----------------------------------------------------------------------


end tb;