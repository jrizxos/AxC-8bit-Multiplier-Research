
--------------------------------------------------------------------------------------
-- Company Name: Department of Computer Science & Engineering / University of Ioannina 

-- Engineer: Georgios Papatheodorou

-- Module: 8x8 Reduced Complexity Wallace Tree Multyplier (Waters - 2010)

-- Module Name: wallace

-- Revisions:
-- 
-- Additional Comments: 
--
--------------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity wallace is
    port ( A0 	 : in  STD_LOGIC_VECTOR (7 downto 0);
           B0 	 : in  STD_LOGIC_VECTOR (7 downto 0);
           prodA : out STD_LOGIC_VECTOR (14 downto 0);
			  prodB : out STD_LOGIC_VECTOR (14 downto 0));
end wallace;


architecture Behavioral of wallace is

component full_adder is
    port ( a		: in  STD_LOGIC;
           b		: in  STD_LOGIC;
           c		: in  STD_LOGIC;
           sum		: out STD_LOGIC;
           carry  : out STD_LOGIC);
end component;


component half_adder is
    port ( a 		: in  STD_LOGIC;
           b 		: in  STD_LOGIC;
           sum		: out STD_LOGIC;
           carry 	: out STD_LOGIC);
end component;

signal s1012,s1011,s1010,s1009,s1008,s1007,s1006,s1005,s1004,s1003,
s1002,s1109,s1108,s1107,s1106,s1105,s2012,s2011,s2010,s2009,s2008,
s2007,s2006,s2005,s2004,s2003,s2108,s2107,s3012,s3010,s3009,s3008,
s3007,s3006,s3004,s24011,s24010,s24009,s24008,s24007,s24006,s4005,  
s0002,s4006,s4007,s4008,s4009,s4010,s4011  : std_logic; --42


signal c1012,c1011,c1010,c1009,c1008,c1007,c1006,c1005,c1004,c1003,
c1002,c1109,c1108,c1107,c1106,c1105,c2012,c2011,c2010,c2009,c2008,
c2007,c2006,c2005,c2004,c2003,c2108,c2107,c3012,c3010,c3009,c3008,
c3007,c3006,c3004,c4011,c4010,c4009,c4008,c4007,c4006,c4005 : std_logic; --42

signal p000,p010,p020,p030,p040,p050,p060,p070  : std_logic_vector(7 downto 0);

begin


process(A0,B0)
begin
    for i in 0 to 7 loop
        p000(i) <= A0(i) and B0(0);
        p010(i) <= A0(i) and B0(1);
        p020(i) <= A0(i) and B0(2);
        p030(i) <= A0(i) and B0(3);
		  p040(i) <= A0(i) and B0(4);
		  p050(i) <= A0(i) and B0(5);
		  p060(i) <= A0(i) and B0(6);
		  p070(i) <= A0(i) and B0(7);
    end loop;       
end process;

prodA(0)  <= p000(0);
prodA(1)  <= p000(1);
prodA(2)  <= s0002;
prodA(3)  <= s2003;
prodA(4)  <= s3004;
prodA(5)  <= s4005;
prodA(6)  <= s4006;
prodA(7)  <= s4007;
prodA(8)  <= s4008;
prodA(9)  <= s4009;
prodA(10) <= s4010;
prodA(11) <= s4011;
prodA(12) <= s3012;
prodA(13) <= s2012;
prodA(14) <= p070(7);

prodB(0)  <= '0';
prodB(1)  <= p010(0);
prodB(2)  <= '0';
prodB(3)  <= '0';
prodB(4)  <= '0';
prodB(5)  <= '0';
prodB(6)  <= c4005;
prodB(7)  <= c4006;
prodB(8)  <= c4007;
prodB(9)  <= c4008;
prodB(10) <= c4009;
prodB(11) <= c4010;
prodB(12) <= c4011;
prodB(13) <= c3012;
prodB(14) <= c2012;
    
--prod(0) <= p0(0);
--prod(1) <= s11;
--prod(2) <= s22;
--prod(3) <= s33;
--prod(4) <= s34;
--prod(5) <= s35;
--prod(6) <= s36;
--prod(7) <= s37;
--prod(8) <= c37;


--first stage (16FA, 0HA)
----GROUP 0
fa1002 : full_adder port map(p000(2),p010(1),p020(0),s1002,c1002);
fa1003 : full_adder port map(p000(3),p010(2),p020(1),s1003,c1003);
fa1004 : full_adder port map(p000(4),p010(3),p020(2),s1004,c1004);
fa1005 : full_adder port map(p000(5),p010(4),p020(3),s1005,c1005);
fa1006 : full_adder port map(p000(6),p010(5),p020(4),s1006,c1006);
fa1007 : full_adder port map(p000(7),p010(6),p020(5),s1007,c1007);
fa1008 : full_adder port map(p010(7),p020(6),p030(5),s1008,c1008);
fa1009 : full_adder port map(p020(7),p030(6),p040(5),s1009,c1009);
fa1010 : full_adder port map(p030(7),p040(6),p050(5),s1010,c1010);
fa1011 : full_adder port map(p040(7),p050(6),p060(5),s1011,c1011);
fa1012 : full_adder port map(p050(7),p060(6),p070(5),s1012,c1012);
----GROUP 1
fa1105 : full_adder port map(p030(2),p040(1),p050(0),s1105,c1105);
fa1106 : full_adder port map(p030(3),p040(2),p050(1),s1106,c1106);
fa1107 : full_adder port map(p030(4),p040(3),p050(2),s1107,c1107);
fa1108 : full_adder port map(p040(4),p050(3),p060(2),s1108,c1108);
fa1109 : full_adder port map(p050(4),p060(3),p070(2),s1109,c1109);


--second stage
----GROUP 0
fa2003 : full_adder port map(s1003,c1002,p030(0),s2003,c2003);
fa2004 : full_adder port map(s1004,c1003,p030(1),s2004,c2004);
fa2005 : full_adder port map(s1005,c1004,s1105,s2005,c2005);
fa2006 : full_adder port map(s1006,c1005,s1106,s2006,c2006);
fa2007 : full_adder port map(s1007,c1006,s1107,s2007,c2007);
fa2008 : full_adder port map(s1008,c1007,s1108,s2008,c2008);
fa2009 : full_adder port map(s1009,c1008,s1109,s2009,c2009);
fa2010 : full_adder port map(s1010,c1009,p060(4),s2010,c2010);
fa2011 : full_adder port map(s1011,c1010,p070(4),s2011,c2011);
fa2012 : full_adder port map(p060(7),c1012,p070(6),s2012,c2012);
----GROUP 1
fa2107 : full_adder port map(c1106,p060(1),p070(0),s2107,c2107);
ha2108 : half_adder port map(c1107,p070(1),s2108,c2108);


--third stage
----GROUP 0
fa3004 : full_adder port map(s2004,c2003,p040(0),s3004,c3004);
fa3006 : full_adder port map(s2006,c2005,c1105,s3006,c3006);
fa3007 : full_adder port map(s2007,c2006,s2107,s3007,c3007);
fa3008 : full_adder port map(s2008,c2007,s2108,s3008,c3008);
fa3009 : full_adder port map(s2009,c2008,c1108,s3009,c3009);
fa3010 : full_adder port map(s2010,c2009,c1109,s3010,c3010);
fa3012 : full_adder port map(s2012,c2011,c1011,s3012,c3012);


--fourth stage
----GROUP 0
fa4005 : full_adder port map(s2005,c2004,c3004,s4005,c4005);
ha4006 : half_adder port map(s3006,p060(0),s4006,c4006);
ha4007 : half_adder port map(s3007,c3006,s4007,c4007);
fa4008 : full_adder port map(s3008,c3007,c2107,s4008,c4008);
fa4009 : full_adder port map(s3009,c3008,c2108,s4009,c4009);
fa4010 : full_adder port map(s3010,c3009,p070(3),s4010,c4010);
fa4011 : full_adder port map(s2011,c2010,c3010,s4011,c4011);

----first stage
--ha11 : half_adder port map(p0(1),p1(0),s11,c11);
--fa12 : full_adder port map(p0(2),p1(1),p2(0),s12,c12);
--fa13 : full_adder port map(p0(3),p1(2),p2(1),s13,c13);
--fa14 : full_adder port map(p1(3),p2(2),p3(1),s14,c14);
--ha15 : half_adder port map(p2(3),p3(2),s15,c15);
--
----second stage
--ha22 : half_adder port map(c11,s12,s22,c22);
--fa23 : full_adder port map(p3(0),c12,s13,s23,c23);
--ha24 : half_adder port map(c13,s14,s24,c24);
--ha25 : half_adder port map(c14,s15,s25,c25);
--ha26 : half_adder port map(c15,p3(3),s26,c26);
--
----third stage
--ha33 : half_adder port map(c22,s23,s33,c33);
--fa34 : full_adder port map(c23,s24,c33,s34,c34);
--fa35 : full_adder port map(c24,s25,c34,s35,c35);
--fa36 : full_adder port map(c25,s26,c35,s36,c36);
--ha37 : half_adder port map(c36,c26,s37,c37);

end Behavioral;