library ieee;
use ieee.std_logic_1164.all;

entity tb_wallace_test is
end tb_wallace_test;

architecture tb of tb_wallace_test is

    component wallace_test
        port (A    : in std_logic_vector (3 downto 0);
              B    : in std_logic_vector (3 downto 0);
              prod : out std_logic_vector (8 downto 0));-- 7 downto 0 
    end component;

    signal A    : std_logic_vector (3 downto 0);
    signal B    : std_logic_vector (3 downto 0);
    signal prod : std_logic_vector (8 downto 0); -- 7 downto 0 

begin

    dut : wallace_test
	 
    port map (A    => A,
              B    => B,
              prod => prod);
				  

    stimuli : process
	 
    begin
        -- EDIT Adapt initialization as needed
        --A <= (others => '0');
        --B <= (others => '0');

        -- EDIT Add stimuli here
		  
		  -- A 0000
			
			A <= "0000";
			B <= "0000";
			wait for 10 ns;
			
			A <= "0000";
			B <= "0001";
			wait for 10 ns;
			
			A <= "0000";
			B <= "0010";
			wait for 10 ns;
			
			A <= "0000";
			B <= "0011";
			wait for 10 ns;
			
			A <= "0000";
			B <= "0100";
			wait for 10 ns;
			
			A <= "0000";
			B <= "0101";
			wait for 10 ns;
			
			A <= "0000";
			B <= "0110";
			wait for 10 ns;
			
			A <= "0000";
			B <= "0111";
			wait for 10 ns;
			
			A <= "0000";
			B <= "1000";
			wait for 10 ns;
			
			A <= "0000";
			B <= "1001";
			wait for 10 ns;
			
			A <= "0000";
			B <= "1010";
			wait for 10 ns;
			
			A <= "0000";
			B <= "1011";
			wait for 10 ns;
			
			A <= "0000";
			B <= "1100";
			wait for 10 ns;
			
			A <= "0000";
			B <= "1101";
			wait for 10 ns;
			
			A <= "0000";
			B <= "1110";
			wait for 10 ns;
			
			A <= "0000";
			B <= "1111";
			wait for 10 ns;

	
	-- A 0001
			
			A <= "0001";
			B <= "0000";
			wait for 10 ns;
			
			A <= "0001";
			B <= "0001";
			wait for 10 ns;
			
			A <= "0001";
			B <= "0010";
			wait for 10 ns;
			
			A <= "0001";
			B <= "0011";
			wait for 10 ns;
			
			A <= "0001";
			B <= "0100";
			wait for 10 ns;
			
			A <= "0001";
			B <= "0101";
			wait for 10 ns;
			
			A <= "0001";
			B <= "0110";
			wait for 10 ns;
			
			A <= "0001";
			B <= "0111";
			wait for 10 ns;
			
			A <= "0001";
			B <= "1000";
			wait for 10 ns;
			
			A <= "0001";
			B <= "1001";
			wait for 10 ns;
			
			A <= "0001";
			B <= "1010";
			wait for 10 ns;
			
			A <= "0001";
			B <= "1011";
			wait for 10 ns;
			
			A <= "0001";
			B <= "1100";
			wait for 10 ns;
			
			A <= "0001";
			B <= "1101";
			wait for 10 ns;
			
			A <= "0001";
			B <= "1110";
			wait for 10 ns;
			
			A <= "0001";
			B <= "1111";
			wait for 10 ns;
			
	-- A 0010
	
			A <= "0010";
			B <= "0000";
			wait for 10 ns;
			
			A <= "0010";
			B <= "0001";
			wait for 10 ns;
			
			A <= "0010";
			B <= "0010";
			wait for 10 ns;
			
			A <= "0010";
			B <= "0011";
			wait for 10 ns;
			
			A <= "0010";
			B <= "0100";
			wait for 10 ns;
			
			A <= "0010";
			B <= "0101";
			wait for 10 ns;
			
			A <= "0010";
			B <= "0110";
			wait for 10 ns;
			
			A <= "0010";
			B <= "0111";
			wait for 10 ns;
			
			A <= "0010";
			B <= "1000";
			wait for 10 ns;
			
			A <= "0010";
			B <= "1001";
			wait for 10 ns;
			
			A <= "0010";
			B <= "1010";
			wait for 10 ns;
			
			A <= "0010";
			B <= "1011";
			wait for 10 ns;
			
			A <= "0010";
			B <= "1100";
			wait for 10 ns;
			
			A <= "0010";
			B <= "1101";
			wait for 10 ns;
			
			A <= "0010";
			B <= "1110";
			wait for 10 ns;
			
			A <= "0010";
			B <= "1111";
			wait for 10 ns;
			
	-- A 0011
			
			A <= "0011";
			B <= "0000";
			wait for 10 ns;
			
			A <= "0011";
			B <= "0001";
			wait for 10 ns;
			
			A <= "0011";
			B <= "0010";
			wait for 10 ns;
			
			A <= "0011";
			B <= "0011";
			wait for 10 ns;
			
			A <= "0011";
			B <= "0100";
			wait for 10 ns;
			
			A <= "0011";
			B <= "0101";
			wait for 10 ns;
			
			A <= "0011";
			B <= "0110";
			wait for 10 ns;
			
			A <= "0011";
			B <= "0111";
			wait for 10 ns;
			
			A <= "0011";
			B <= "1000";
			wait for 10 ns;
			
			A <= "0011";
			B <= "1001";
			wait for 10 ns;
			
			A <= "0011";
			B <= "1010";
			wait for 10 ns;
			
			A <= "0011";
			B <= "1011";
			wait for 10 ns;
			
			A <= "0011";
			B <= "1100";
			wait for 10 ns;
			
			A <= "0011";
			B <= "1101";
			wait for 10 ns;
			
			A <= "0011";
			B <= "1110";
			wait for 10 ns;
			
			A <= "0011";
			B <= "1111";
			wait for 10 ns;
        
		
		--A 0100
		  
		   A <= "0100";
			B <= "0000";
			wait for 10 ns;
			
			A <= "0100";
			B <= "0001";
			wait for 10 ns;
			
			A <= "0100";
			B <= "0010";
			wait for 10 ns;
			
			A <= "0100";
			B <= "0011";
			wait for 10 ns;
			
			A <= "0100";
			B <= "0100";
			wait for 10 ns;
			
			A <= "0100";
			B <= "0101";
			wait for 10 ns;
			
			A <= "0100";
			B <= "0110";
			wait for 10 ns;
			
			A <= "0100";
			B <= "0111";
			wait for 10 ns;
			
			A <= "0100";
			B <= "1000";
			wait for 10 ns;
			
			A <= "0100";
			B <= "1001";
			wait for 10 ns;
			
			A <= "0100";
			B <= "1010";
			wait for 10 ns;
			
			A <= "0100";
			B <= "1011";
			wait for 10 ns;
			
			A <= "0100";
			B <= "1100";
			wait for 10 ns;
			
			A <= "0100";
			B <= "1101";
			wait for 10 ns;
			
			A <= "0100";
			B <= "1110";
			wait for 10 ns;
			
			A <= "0100";
			B <= "1111";
			wait for 10 ns;
			
	
	-- A 0101
	
			A <= "0101";
			B <= "0000";
			wait for 10 ns;
			
			A <= "0101";
			B <= "0001";
			wait for 10 ns;
			
			A <= "0101";
			B <= "0010";
			wait for 10 ns;
			
			A <= "0101";
			B <= "0011";
			wait for 10 ns;
			
			A <= "0101";
			B <= "0100";
			wait for 10 ns;
			
			A <= "0101";
			B <= "0101";
			wait for 10 ns;
			
			A <= "0101";
			B <= "0110";
			wait for 10 ns;
			
			A <= "0101";
			B <= "0111";
			wait for 10 ns;
			
			A <= "0101";
			B <= "1000";
			wait for 10 ns;
			
			A <= "0101";
			B <= "1001";
			wait for 10 ns;
			
			A <= "0101";
			B <= "1010";
			wait for 10 ns;
			
			A <= "0101";
			B <= "1011";
			wait for 10 ns;
			
			A <= "0101";
			B <= "1100";
			wait for 10 ns;
			
			A <= "0101";
			B <= "1101";
			wait for 10 ns;
			
			A <= "0101";
			B <= "1110";
			wait for 10 ns;
			
			A <= "0101";
			B <= "1111";
			wait for 10 ns;
			
	-- A 0110
	
			A <= "0110";
			B <= "0000";
			wait for 10 ns;
			
			A <= "0110";
			B <= "0001";
			wait for 10 ns;
			
			A <= "0110";
			B <= "0010";
			wait for 10 ns;
			
			A <= "0110";
			B <= "0011";
			wait for 10 ns;
			
			A <= "0110";
			B <= "0100";
			wait for 10 ns;
			
			A <= "0110";
			B <= "0101";
			wait for 10 ns;
			
			A <= "0110";
			B <= "0110";
			wait for 10 ns;
			
			A <= "0110";
			B <= "0111";
			wait for 10 ns;
			
			A <= "0110";
			B <= "1000";
			wait for 10 ns;
			
			A <= "0110";
			B <= "1001";
			wait for 10 ns;
			
			A <= "0110";
			B <= "1010";
			wait for 10 ns;
			
			A <= "0110";
			B <= "1011";
			wait for 10 ns;
			
			A <= "0110";
			B <= "1100";
			wait for 10 ns;
			
			A <= "0110";
			B <= "1101";
			wait for 10 ns;
			
			A <= "0110";
			B <= "1110";
			wait for 10 ns;
			
			A <= "0110";
			B <= "1111";
			wait for 10 ns;
	
	-- A 0111
	
			A <= "0111";
			B <= "0000";
			wait for 10 ns;
			
			A <= "0111";
			B <= "0001";
			wait for 10 ns;
			
			A <= "0111";
			B <= "0010";
			wait for 10 ns;
			
			A <= "0111";
			B <= "0011";
			wait for 10 ns;
			
			A <= "0111";
			B <= "0100";
			wait for 10 ns;
			
			A <= "0111";
			B <= "0101";
			wait for 10 ns;
			
			A <= "0111";
			B <= "0110";
			wait for 10 ns;
			
			A <= "0111";
			B <= "0111";
			wait for 10 ns;
			
			A <= "0111";
			B <= "1000";
			wait for 10 ns;
			
			A <= "0111";
			B <= "1001";
			wait for 10 ns;
			
			A <= "0111";
			B <= "1010";
			wait for 10 ns;
			
			A <= "0111";
			B <= "1011";
			wait for 10 ns;
			
			A <= "0111";
			B <= "1100";
			wait for 10 ns;
			
			A <= "0111";
			B <= "1101";
			wait for 10 ns;
			
			A <= "0111";
			B <= "1110";
			wait for 10 ns;
			
			A <= "0111";
			B <= "1111";
			wait for 10 ns;
			
	-- A 1000
	
			A <= "1000";
			B <= "0000";
			wait for 10 ns;
			
			A <= "1000";
			B <= "0001";
			wait for 10 ns;
			
			A <= "1000";
			B <= "0010";
			wait for 10 ns;
			
			A <= "1000";
			B <= "0011";
			wait for 10 ns;
			
			A <= "1000";
			B <= "0100";
			wait for 10 ns;
			
			A <= "1000";
			B <= "0101";
			wait for 10 ns;
			
			A <= "1000";
			B <= "0110";
			wait for 10 ns;
			
			A <= "1000";
			B <= "0111";
			wait for 10 ns;
			
			A <= "1000";
			B <= "1000";
			wait for 10 ns;
			
			A <= "1000";
			B <= "1001";
			wait for 10 ns;
			
			A <= "1000";
			B <= "1010";
			wait for 10 ns;
			
			A <= "1000";
			B <= "1011";
			wait for 10 ns;
			
			A <= "1000";
			B <= "1100";
			wait for 10 ns;
			
			A <= "1000";
			B <= "1101";
			wait for 10 ns;
			
			A <= "1000";
			B <= "1110";
			wait for 10 ns;
			
			A <= "1000";
			B <= "1111";
			wait for 10 ns;
			
			
	-- A 1001
			
			A <= "1001";
			B <= "0000";
			wait for 10 ns;
			
			A <= "1001";
			B <= "0001";
			wait for 10 ns;
			
			A <= "1001";
			B <= "0010";
			wait for 10 ns;
			
			A <= "1001";
			B <= "0011";
			wait for 10 ns;
			
			A <= "1001";
			B <= "0100";
			wait for 10 ns;
			
			A <= "1001";
			B <= "0101";
			wait for 10 ns;
			
			A <= "1001";
			B <= "0110";
			wait for 10 ns;
			
			A <= "1001";
			B <= "0111";
			wait for 10 ns;
			
			A <= "1001";
			B <= "1000";
			wait for 10 ns;
			
			A <= "1001";
			B <= "1001";
			wait for 10 ns;
			
			A <= "1001";
			B <= "1010";
			wait for 10 ns;
			
			A <= "1001";
			B <= "1011";
			wait for 10 ns;
			
			A <= "1001";
			B <= "1100";
			wait for 10 ns;
			
			A <= "1001";
			B <= "1101";
			wait for 10 ns;
			
			A <= "1001";
			B <= "1110";
			wait for 10 ns;
			
			A <= "1001";
			B <= "1111";
			wait for 10 ns;
			
			
	-- A 1010
			
			A <= "1010";
			B <= "0000";
			wait for 10 ns;
			
			A <= "1010";
			B <= "0001";
			wait for 10 ns;
			
			A <= "1010";
			B <= "0010";
			wait for 10 ns;
			
			A <= "1010";
			B <= "0011";
			wait for 10 ns;
			
			A <= "1010";
			B <= "0100";
			wait for 10 ns;
			
			A <= "1010";
			B <= "0101";
			wait for 10 ns;
			
			A <= "1010";
			B <= "0110";
			wait for 10 ns;
			
			A <= "1010";
			B <= "0111";
			wait for 10 ns;
			
			A <= "1010";
			B <= "1000";
			wait for 10 ns;
			
			A <= "1010";
			B <= "1001";
			wait for 10 ns;
			
			A <= "1010";
			B <= "1010";
			wait for 10 ns;
			
			A <= "1010";
			B <= "1011";
			wait for 10 ns;
			
			A <= "1010";
			B <= "1100";
			wait for 10 ns;
			
			A <= "1010";
			B <= "1101";
			wait for 10 ns;
			
			A <= "1010";
			B <= "1110";
			wait for 10 ns;
			
			A <= "1010";
			B <= "1111";
			wait for 10 ns;
			
			
	-- A 1011
	
			A <= "1011";
			B <= "0000";
			wait for 10 ns;
			
			A <= "1011";
			B <= "0001";
			wait for 10 ns;
			
			A <= "1011";
			B <= "0010";
			wait for 10 ns;
			
			A <= "1011";
			B <= "0011";
			wait for 10 ns;
			
			A <= "1011";
			B <= "0100";
			wait for 10 ns;
			
			A <= "1011";
			B <= "0101";
			wait for 10 ns;
			
			A <= "1011";
			B <= "0110";
			wait for 10 ns;
			
			A <= "1011";
			B <= "0111";
			wait for 10 ns;
			
			A <= "1011";
			B <= "1000";
			wait for 10 ns;
			
			A <= "1011";
			B <= "1001";
			wait for 10 ns;
			
			A <= "1011";
			B <= "1010";
			wait for 10 ns;
			
			A <= "1011";
			B <= "1011";
			wait for 10 ns;
			
			A <= "1011";
			B <= "1100";
			wait for 10 ns;
			
			A <= "1011";
			B <= "1101";
			wait for 10 ns;
			
			A <= "1011";
			B <= "1110";
			wait for 10 ns;
			
			A <= "1011";
			B <= "1111";
			wait for 10 ns;
			
			
	-- A 1100
	
			A <= "1100";
			B <= "0000";
			wait for 10 ns;
			
			A <= "1100";
			B <= "0001";
			wait for 10 ns;
			
			A <= "1100";
			B <= "0010";
			wait for 10 ns;
			
			A <= "1100";
			B <= "0011";
			wait for 10 ns;
			
			A <= "1100";
			B <= "0100";
			wait for 10 ns;
			
			A <= "1100";
			B <= "0101";
			wait for 10 ns;
			
			A <= "1100";
			B <= "0110";
			wait for 10 ns;
			
			A <= "1100";
			B <= "0111";
			wait for 10 ns;
			
			A <= "1100";
			B <= "1000";
			wait for 10 ns;
			
			A <= "1100";
			B <= "1001";
			wait for 10 ns;
			
			A <= "1100";
			B <= "1010";
			wait for 10 ns;
			
			A <= "1100";
			B <= "1011";
			wait for 10 ns;
			
			A <= "1100";
			B <= "1100";
			wait for 10 ns;
			
			A <= "1100";
			B <= "1101";
			wait for 10 ns;
			
			A <= "1100";
			B <= "1110";
			wait for 10 ns;
			
			A <= "1100";
			B <= "1111";
			wait for 10 ns;
			
	-- A 1101
	
			A <= "1101";
			B <= "0000";
			wait for 10 ns;
			
			A <= "1101";
			B <= "0001";
			wait for 10 ns;
			
			A <= "1101";
			B <= "0010";
			wait for 10 ns;
			
			A <= "1101";
			B <= "0011";
			wait for 10 ns;
			
			A <= "1101";
			B <= "0100";
			wait for 10 ns;
			
			A <= "1101";
			B <= "0101";
			wait for 10 ns;
			
			A <= "1101";
			B <= "0110";
			wait for 10 ns;
			
			A <= "1101";
			B <= "0111";
			wait for 10 ns;
			
			A <= "1101";
			B <= "1000";
			wait for 10 ns;
			
			A <= "1101";
			B <= "1001";
			wait for 10 ns;
			
			A <= "1101";
			B <= "1010";
			wait for 10 ns;
			
			A <= "1101";
			B <= "1011";
			wait for 10 ns;
			
			A <= "1101";
			B <= "1100";
			wait for 10 ns;
			
			A <= "1101";
			B <= "1101";
			wait for 10 ns;
			
			A <= "1101";
			B <= "1110";
			wait for 10 ns;
			
			A <= "1101";
			B <= "1111";
			wait for 10 ns;
			
			
	-- A 1110
	
	
			A <= "1110";
			B <= "0000";
			wait for 10 ns;
			
			A <= "1110";
			B <= "0001";
			wait for 10 ns;
			
			A <= "1110";
			B <= "0010";
			wait for 10 ns;
			
			A <= "1110";
			B <= "0011";
			wait for 10 ns;
			
			A <= "1110";
			B <= "0100";
			wait for 10 ns;
			
			A <= "1110";
			B <= "0101";
			wait for 10 ns;
			
			A <= "1110";
			B <= "0110";
			wait for 10 ns;
			
			A <= "1110";
			B <= "0111";
			wait for 10 ns;
			
			A <= "1110";
			B <= "1000";
			wait for 10 ns;
			
			A <= "1110";
			B <= "1001";
			wait for 10 ns;
			
			A <= "1110";
			B <= "1010";
			wait for 10 ns;
			
			A <= "1110";
			B <= "1011";
			wait for 10 ns;
			
			A <= "1110";
			B <= "1100";
			wait for 10 ns;
			
			A <= "1110";
			B <= "1101";
			wait for 10 ns;
			
			A <= "1110";
			B <= "1110";
			wait for 10 ns;
			
			A <= "1110";
			B <= "1111";
			wait for 10 ns;
			
			
	-- A 1111
	
			A <= "1111";
			B <= "0000";
			wait for 10 ns;
			
			A <= "1111";
			B <= "0001";
			wait for 10 ns;
			
			A <= "1111";
			B <= "0010";
			wait for 10 ns;
			
			A <= "1111";
			B <= "0011";
			wait for 10 ns;
			
			A <= "1111";
			B <= "0100";
			wait for 10 ns;
			
			A <= "1111";
			B <= "0101";
			wait for 10 ns;
			
			A <= "1111";
			B <= "0110";
			wait for 10 ns;
			
			A <= "1111";
			B <= "0111";
			wait for 10 ns;
			
			A <= "1111";
			B <= "1000";
			wait for 10 ns;
			
			A <= "1111";
			B <= "1001";
			wait for 10 ns;
			
			A <= "1111";
			B <= "1010";
			wait for 10 ns;
			
			A <= "1111";
			B <= "1011";
			wait for 10 ns;
			
			A <= "1111";
			B <= "1100";
			wait for 10 ns;
			
			A <= "1111";
			B <= "1101";
			wait for 10 ns;
			
			A <= "1111";
			B <= "1110";
			wait for 10 ns;
			
			A <= "1111";
			B <= "1111";
			wait for 10 ns;
			
		  wait;
    end process;

end tb;

-- Configuration block below is required by some simulators. Usually no need to edit.

--configuration cfg_tb_wallace_test of tb_wallace_test is
  --  for tb
    --end for;
--end cfg_tb_wallace_test;