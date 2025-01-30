import copy
import math

from Utility.analysis_utils import create_length_equation


class MasterAnalysisObject:
    def __init__(self, problem):
        """
        Initialize the MasterAnalysisObject.

        Parameters:
        - evidence: An object containing a list of words.
        - problem: An object containing sacs_to_solve (list of sacs) and alphabet (with mappings dictionary).
        """
        self.problem = problem
        self.flag = True

        self.min_growth = []
        self.max_growth = []
        self.min_length = []
        self.max_length = []
        self.fragments = []  # List of Fragment objects

        # These numbers get calculated a LOT so store them makes life easier
        self.num_symbols = len(self.problem.evidence.alphabet.symbols)
        self.num_sacs = len(self.problem.evidence.sacs)
        self.num_words = len(self.problem.evidence.words)

        self.min_growth = [[0 for _ in range(self.num_symbols)] for _ in range(self.num_sacs)]
        self.max_growth = [[0 for _ in range(self.num_symbols)] for _ in range(self.num_sacs)]

        self.min_length = [0 for _ in range(self.num_sacs)]
        self.max_length = [0 for _ in range(self.num_sacs)]

        self.symbol_counts = [[0 for _ in range(self.num_symbols)] for _ in range(self.num_words)]
        self.word_unaccounted_growth = [[0 for _ in range(self.num_symbols)] for _ in range(self.num_words-1)]
        self.word_unaccounted_length = [0 for _ in range(self.num_words-1)]

        # the sum of the successors in each word have to be within the min/max of the values stored here
        self.total_length_min = [0 for _ in range(self.num_words-1)]
        self.total_length_max = [0 for _ in range(self.num_words-1)]

        # an equation if a dictionary containing a list of sacs and a value
        # e.g.: { 'sacs' : List[sac], 'value' : int }
        self.length_equations = []

        # Conduct Naive/Initial analysis
        self.naive_min_max()
        self.compute_symbol_counts()

        # Initialize Unaccounted Growth & Length
        self.compute_unaccounted_growth_matrix()
        self.compute_unaccounted_length_matrix()
        self.problem.MAO = self

    def set_min_growth(self, sac, symbol, value):
        if self.min_growth[self.problem.evidence.get_sac_id(sac)][symbol] < value:
            self.min_growth[self.problem.evidence.get_sac_id(sac)][symbol] = value
            self.flag = True

    def set_max_growth(self, sac, symbol, value):
        if self.max_growth[self.problem.evidence.get_sac_id(sac)][symbol] > value:
            self.max_growth[self.problem.evidence.get_sac_id(sac)][symbol] = value
            self.flag = True

    def set_min_length(self, sac, value):
        if self.min_length[self.problem.evidence.get_sac_id(sac)] < value:
            self.min_length[self.problem.evidence.get_sac_id(sac)] = value
            self.flag = True

    def set_max_length(self, sac, value):
        if self.max_length[self.problem.evidence.get_sac_id(sac)] > value:
            self.max_length[self.problem.evidence.get_sac_id(sac)] = value
            self.flag = True

    def set_total_length_min(self, iWord, value):
        if self.total_length_min[iWord] > value:
            self.total_length_min[iWord] = value
            self.flag = True

    def set_total_length_max(self, iWord, value):
        if self.total_length_max[iWord] > value:
            self.total_length_max[iWord] = value
            self.flag = True

    # These get called a lot so it just keeps the code cleaner
    def get_min_growth(self, sac, symbol):
        return self.min_growth[self.problem.evidence.get_sac_id(sac)][symbol]

    def get_max_growth(self, sac, symbol):
        return self.max_growth[self.problem.evidence.get_sac_id(sac)][symbol]

    def get_min_length(self, sac):
        return self.problem.MAO.min_length[self.problem.evidence.get_sac_id(sac)]

    def get_max_length(self, sac):
        return self.problem.MAO.max_length[self.problem.evidence.get_sac_id(sac)]

    def is_symbol_id_identity(self, id):
        return id in self.problem.evidence.alphabet.identities_ids

    def is_symbol_identity(self, symbol):
        return symbol in self.problem.evidence.alphabet.identities

    def is_sac_identity(self, sac):
        return sac.symbol in self.problem.evidence.alphabet.identities_ids

    def get_variable_sacs(self, w):
         return [(key, value) for key, value in w.sacs.items() if not self.is_sac_identity(key)]

    def get_variable_sac_counts(self, w):
         return [(key, value) for key, value in w.sac_counts.items() if not self.is_sac_identity(key)]

    def get_identity_sacs(self, w):
         return [(key, value) for key, value in w.sacs.items() if self.is_sac_identity(key)]

    def get_identity_sac_counts(self, w):
         return [(key, value) for key, value in w.sac_counts.items() if self.is_sac_identity(key)]

    # The following functions compute some kind of fact that helps reduce the p-space size.
    def compute_lexicon(self):
        pass

    def compute_length_absolute_min_max(self):
        """
        Computes the absolute minimum and maximum lengths for each symbol in evidence.
        """
        print("\nComputing Absolute Min/Max Length")
        for iWord, w in enumerate(self.problem.evidence.words[:-1]):
            reserve_right = 0
            reserve_left = 0

            # Compute reserve_right
            for iSac, sac in enumerate(w):
                if sac.symbol not in self.problem.evidence.alphabet.identities_ids:
                    reserve_right += self.problem.absolute_min_length
                else:
                    reserve_right += 1

            # Compute Min/Max Length for each position
            for iSac, sac in enumerate(w):
                max_length = len(self.problem.evidence.words[iWord+1]) - (reserve_left + reserve_right)
                if sac.symbol not in self.problem.evidence.alphabet.identities_ids:
                    self.set_max_length(sac, max_length)
                    reserve_right -= self.problem.absolute_min_length
                    reserve_left += self.problem.absolute_min_length
                else:
                    reserve_right -= 1
                    reserve_left += 1

    def compute_absolute_minmax_growth(self):
        """
        Look at the growth
        For max, no symbol can produce more than the complete growth from one generation to another
        For min, no growth at all
        """
        print("\nComputing Absolute Min/Max Growth")
        pass

    def compute_length_total_symbol_production(self):
        """
        Computes the minimum and maximum lengths of symbols in W1 based on their
        contributions to the total length of W2.
        """
        for iWord, w in enumerate(self.problem.evidence.words[:-1]):
            total_length = len(self.problem.evidence.words[iWord+1])
            for sac1, count1 in w.sac_counts.items():
                produced_min = 0
                produced_max = 0
                # no need to do this calculation for symbols with identity
                for sac2, count2 in w.sac_counts.items():
                    # for every other sac compute how much they produce
                    if sac1 != sac2:
                        produced_min += count2 * self.problem.MAO.get_min_length(sac2)
                        produced_max += count2 * self.problem.MAO.get_max_length(sac2)

                remainder_min = max(0,total_length - produced_max)
                remainder_max = max(0,total_length - produced_min)

                min_length = remainder_min / count1
                max_length = remainder_max / count1

                self.problem.MAO.set_min_length(sac1, min_length)
                self.problem.MAO.set_max_length(sac1, max_length)

    def compute_total_length_total_symbol_production(self, include_identities=False):
        """
        Find the SAC that appear least and most frequently
        Max total length is the sum of the least frequent handling the most # of symbols + max of the rest
        Min total length is the sum of the most frequent handling the most # of symbols + min of the rest
        """

        # Get the list of SaCs that occur the least and most frequently (but actually exist)
        for iWord, w in enumerate(self.problem.evidence.words[:-1]):
            # get the sacs that occur most/least frequently

            word_sac_counts = self.get_variable_sac_counts(w)
            sorted_items = sorted(word_sac_counts, key=lambda x: x[1], reverse=True)
            max_value = sorted_items[0][1]
            sorted_items = sorted(word_sac_counts, key=lambda x: x[1])
            min_value = sorted_items[0][1]

            most_frequent = [(key, value) for key, value in word_sac_counts if value == max_value]
            least_frequent = [(key, value) for key, value in word_sac_counts if value == min_value]

            # The unaccounted for growth must not include that from variables, only identities
            uag_total = sum(self.symbol_counts[iWord+1])
            if not include_identities:
                # Subtract out identities from iWord
                for iSymbol, count in enumerate(self.symbol_counts[iWord]):
                    if self.is_symbol_id_identity(iSymbol):
                        uag_total -= count

            for iMost, most in enumerate(most_frequent):
                if not self.is_symbol_id_identity(most[0].symbol) or include_identities:
                    for iLeast, least in enumerate(least_frequent):
                        if most[0] != least[0] and (not self.is_symbol_id_identity(least[0].symbol) or include_identities):
                            remainder_max = uag_total
                            remainder_min = uag_total
                            rest_min = 0
                            rest_max = 0

                            # Max total length is the sum of the least frequent handling the most # of symbols + max of the rest
                            # Min total length is the sum of the most frequent handling the least # of symbols + min of the rest
                            for sac, count in self.problem.evidence.words[iWord].sac_counts.items():
                                # do not include the sac that occurs the most, and do not include identities (unless specified)
                                if most[0] != sac and (not self.is_symbol_id_identity(sac.symbol) or include_identities):
                                    remainder_min -= count * self.get_min_length(sac)
                                    rest_min += self.get_min_length(sac)
                                # do not include the sac that occurs the least, and do not include identities (unless specified)
                                if least[0] != sac and (not self.is_symbol_id_identity(sac.symbol) or include_identities):
                                    remainder_max -= count * self.get_max_length(sac)
                                    rest_max += self.get_max_length(sac)
                            total_min = rest_min + remainder_min / self.problem.evidence.words[iWord].sac_counts[most[0]]
                            total_max = rest_max + max(0,remainder_max) / self.problem.evidence.words[iWord].sac_counts[least[0]]

                            # subtract out the length of the identities
                            if include_identities:
                                identity_counts = self.get_identity_sac_counts(w)
                                total_identity_count = len(identity_counts)
                                total_min -= total_identity_count
                                total_max -= total_identity_count

                            self.set_total_length_max(iWord, total_max)
                            self.set_total_length_min(iWord, total_min)

    def compute_total_length_symbiology(self):
        pass

    def compute_total_length_by_length(self):
        pass


    def compute_length_total_length(self):
        """
        For wi => wi+1 Assume that all symbols except one provide their min/max, the remaining symbol must produce
        the remainder
        :return:
        """
        pass

    def compute_length_symbiology(self):
        pass

    def compute_growth_symbiology(self):
        """
        Analyze growth pattern
        A. a SAC does not produce a symbol S if the growth of S = 0 in the generation immediately following it
        B. if growth is constant for a symbol S1, than any symbols that appeared in the previous generation did not produce the symbol S1 unless a symbol has vanished which may have produced S1
        Example, if Growth of A is 4 for G1 => G2 and is still 4 for G2 => G3 then if SAC B appeared in G2 it does not produce A unless another SAC appeared in G2 with G,max(A) > 0
        """
        pass

    def compute_growth_unaccounted_growth(self):
        """
        Scan the evidence, capture how often each symbol + condition exists, reduce growth for the turtles
        For each symbol, reduce the growth by the minimum
        The maximum growth for each symbol, is the min growth + unaccounted for growth divided by the count of number of symbols
        """
        pass

    def compute_growth_total_growth(self):
        """
        works similar to total length
        if a total of 7As are produced and 4As are produced max by all but one symbol then the remaining symbol produces 3
        also, if all the growths are known except one then the remaining symbol must produce everything else
        """
        pass

    def compute_length_growth(self):
        pass

    def compute_fragments_position(self):
        pass

    def compute_growth_fragment(self):
        pass

    def compute_BTF_cache(self):
        pass

    def compute_fragments_revise(self):
        pass

    def compute_lexicon(self):
        """
        find the symbols adjacent to each other
        """
        pass

    def compute_localization_analyze(self):
        """
        void LSIProblemV3::ComputeSymbolLocalization_Analyze(Int32 iGen)
        {
        	// LOCALIZATION ANALYSIS
        	// STEP 1 - This step remove reduces the number of localizations.
        	// A1. If a turtle only options is a position, then no other symbol can produce that turtle
        	// A2. If a turtle can only be produced in a single spot it must be produced in that spot
        	// Example:  +: X(4) +(5) <---- remove this
        	//           +: +(5)   <---- because this must the localization
        	// B1. A symbol cannot be localized to a position if the next position does not have a localization equal or greater than the current symbol
        	// Example: Sn   : 4,5,6 <---- remove the 6
        	//          Sn+1 : 4,5
        	// then Sn cannot be localized to symbol 6
        	// B2. A symbol cannot be localized to a position if the previous position does not have a localization equal or greater than the current symbol
        	// Example: Sn   : 5,6
        	//          Sn+1 : 4,5,6 <--- remove the 4
        	// C1. No symbol can be localized after the last localization of the previous symbol
        	// C2. No symbol can be localized before the first localization of the next symbol

        	// STEP 2 - these steps should finalize the localization settings, i.e. converting 1s to 2s or 1s to 0s
        	// A1. If a symbol has any value is locked then remove the remainder
        	// Example: Sn: 4,5*,6  <---- remove the 4 and 6
        	// A2. If a symbol has only a single precedessor set it to 2

        	// Repeat Steps 1 & 2 until convergence

        	// STEP 3 - these steps discovery facts about the L-system, such as fragments
        	// A. if a set of symbols can only be produced by one symbol, then that set is a fragment
        	// i. if the uniqueness is at the start of the production it is a head fragment
        	// ii. if the uniqueness is at the end of the production it is a tail fragment
        	// iii. if the uniqueness is at the middle of the production it is a mid fragment
        	// iv. if the uniqueness is at the start and end of the production it is a complete fragment
        	// B. Remove any fragment which could not be localized into a wake, mark as tabu

        	// STEP 1 - This step remove reduces the number of localizations repeat until convergence
        	bool change = false;

        	do
        	{
        		change = false;

        		// A1. If a turtle only options is a position, then no other symbol can produce that turtle
        		// Example: +: 4
        		// Example: +: 4,5
        		// Example: +: 5,6  <--- if this is the only option for 6 then 6 must produce this, so remove 5
        		for (Int32 iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
        		{
        			// Do process for A1
        			if (this->model->alphabet->IsTurtle(this->model->evidence[iGen]->GetSymbolIndex(iPos1)))
        			{
        				Int32 count = 0;
        				Int32 idx = 0;
        				Int32 iPos2 = 0;
        				while ((count < 2) && (iPos2 < this->model->evidence[iGen + 1]->Length()))
        				{
        					if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked))
        					{
        						count++;
        						idx = iPos2;
        					}
        					iPos2++;
        				}

        				if (count == 1)
        				{
        					for (size_t iPos3 = 0; iPos3 < this->model->evidence[iGen]->Length(); iPos3++)
        					{
        						if ((this->MAO->localization[iGen][idx, iPos3] == MasterAnalysisObject::cLocalization_Strong) && (iPos1 != iPos3))
        						{
        							//Console::WriteLine("Setting to false " + this->model->evidence[iGen + 1]->GetSymbol(iPos3) + " : " + this->model->evidence[iGen]->GetSymbol(idx) + "(" + idx+ ")");
        							this->MAO->SetLocalization(iGen, idx, iPos3, MasterAnalysisObject::cLocalization_Never);
        							change = true;
        						}
        						else if ((this->MAO->localization[iGen][idx, iPos3] == MasterAnalysisObject::cLocalization_Locked) && (iPos1 != iPos3))
        						{
        							Console::WriteLine("Uh oh!");
        						}
        					}
        				}
        			}

        			// Do process for C1 & C2. Find the first and last occurance for each symbol
        			Int32 first = -1;
        			Int32 last = 0;
        			Int32 iPos2 = 0;
        			bool locked = false;

        			while ((!locked) && (iPos2 < this->model->evidence[iGen + 1]->Length()))
        			{
        				if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong) && (first == -1) && (!locked))
        				{
        					first = iPos2;
        				}

        				if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong) && (!locked))
        				{
        					last = iPos2;
        				}

        				if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
        				{
        					first = iPos2;
        					last = iPos2;
        					locked = true;
        				}
        				iPos2++;
        			}

        			// C1. No symbol can be localized after the last localization of the previous symbol
        			// Example:  Sn: 3,4 <--- if this is the last instance of 4
        			//           Sn+1: 3,5 <--- remove the 3
        			for (size_t iPos2 = last + 1; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
        			{
        				for (Int32 iPos3 = 0; iPos3 < Math::Max(0, iPos1 - 1); iPos3++)
        				{
        					this->MAO->SetLocalization(iGen, iPos2, iPos3, MasterAnalysisObject::cLocalization_Never);
        					//this->MAO->localization[iGen][iPos2, iPos3] == cLocalization_Unset;
        				}
        			}

        			// C2. No symbol can be localized before the first localization of the next symbol
        			// Example:  Sn: 3,5 <--- remove the 5
        			//           Sn+1: 3,4 <--- if this is the first instance of 4
        			for (size_t iPos2 = 0; iPos2 < Math::Max(0, first - 1); iPos2++)
        			{
        				for (size_t iPos3 = iPos1 + 1; iPos3 < this->model->evidence[iGen]->Length(); iPos3++)
        				{
        					this->MAO->SetLocalization(iGen, iPos2, iPos3, MasterAnalysisObject::cLocalization_Never);
        					//this->MAO->localization[iGen][iPos2, iPos3] == cLocalization_Unset;
        				}
        			}
        		}

        		for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
        		{
        			// A2. If a turtle can only be produced by a turtle, then it must be produced by that turtle
        			if (this->model->alphabet->IsTurtle(this->model->evidence[iGen + 1]->GetSymbolIndex(iPos2)))
        			{
        				Int32 count = 0;
        				Int32 idx = 0;
        				Int32 iPos1 = 0;
        				while ((count < 2) && (iPos1 < this->model->evidence[iGen]->Length()))
        				{
        					if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked))
        					{
        						count++;
        						idx = iPos1;
        					}
        					iPos1++;
        				}

        				// if the turtle can only be produced by a single turtle then eliminate all other possibilities
        				if ((count == 1) && (this->model->alphabet->IsTurtle(this->model->evidence[iGen]->GetSymbolIndex(idx))))
        				{
        					for (size_t iPos3 = 0; iPos3 < this->model->evidence[iGen + 1]->Length(); iPos3++)
        					{
        						if ((this->MAO->localization[iGen][iPos3, idx] == MasterAnalysisObject::cLocalization_Strong) && (iPos2 != iPos3))
        						{
        							this->MAO->SetLocalization(iGen, iPos3, idx, MasterAnalysisObject::cLocalization_Never);
        							change = true;
        						}
        						else if ((this->MAO->localization[iGen][iPos3, idx] == MasterAnalysisObject::cLocalization_Locked) && (iPos2 != iPos3))
        						{
        							Console::WriteLine("Uh oh!");
        						}
        					}
        				}
        			}

        			// B1. A symbol cannot be localized to a position if the next position does not have a localization equal or greater than the current symbol
        			Int32 largest = 0;
        			Int32 smallest = 999999;
        			for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
        			{
        				if ((iPos2 < this->model->evidence[iGen + 1]->Length() - 1) && ((this->MAO->localization[iGen][iPos2 + 1, iPos1] == MasterAnalysisObject::cLocalization_Strong) || (this->MAO->localization[iGen][iPos2 + 1, iPos1] == MasterAnalysisObject::cLocalization_Locked)) && (iPos1 > largest))
        				{
        					largest = iPos1;
        				}

        				if ((iPos2 > 0) && ((this->MAO->localization[iGen][iPos2 - 1, iPos1] == MasterAnalysisObject::cLocalization_Strong) || (this->MAO->localization[iGen][iPos2 - 1, iPos1] == MasterAnalysisObject::cLocalization_Locked)) && (iPos1 < smallest))
        				{
        					smallest = iPos1;
        				}
        			}

        			// Nothing larger than the largest in the next symbol can produce the current symbol
        			if (iPos2 < this->model->evidence[iGen + 1]->Length() - 1)
        			{
        				for (size_t iPos1 = largest + 1; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
        				{
        					if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong)
        					{
        						this->MAO->SetLocalization(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Never);
        						change = true;
        					}
        					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
        					{
        						Console::WriteLine("Uh oh!");
        					}
        				}
        			}

        			// Nothing smaller than the smallest in the previous symbol can produce the current symbol
        			if (iPos2 > 0)
        			{
        				for (size_t iPos1 = 0; iPos1 < Math::Max(0, smallest - 1); iPos1++)
        				{
        					if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong)
        					{
        						this->MAO->SetLocalization(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Never);
        						change = true;
        					}
        					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
        					{
        						Console::WriteLine("Uh oh!");
        					}
        				}
        			}

        			// STEP 2 - these steps should convert finalize the localization settings, i.e. converting 1s to 2s or 1s to 0s
        			// A1. If a symbol has any value is locked then remove the remainder
        			// A2. If a symbol has only a single precedessor set it to 2
        			Int32 count = 0;
        			Int32 idx = 0;
        			for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
        			{
        				if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
        				{
        					for (size_t iPos3 = 0; iPos3 < this->model->evidence[iGen]->Length(); iPos3++)
        					{
        						if ((iPos1 != iPos3) && (this->MAO->localization[iGen][iPos2, iPos3] != MasterAnalysisObject::cLocalization_Never))
        						{
        							this->MAO->SetLocalization(iGen, iPos2, iPos3, MasterAnalysisObject::cLocalization_Never);
        							change = true;
        						}
        					}
        				}
        				else if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked))
        				{
        					count++;
        					idx = iPos1;
        				}
        			}

        			if (count == 1)
        			{
        				this->MAO->SetLocalization(iGen, iPos2, idx, MasterAnalysisObject::cLocalization_Locked);
        				change = true;
        			}
        		}
        	} while (change);
        }
        """
        pass

    def compute_localization_analyze_BTFonly(self):
        """
        void LSIProblemV3::ComputeSymbolLocalization_Analyze_BTFOnly(Int32 iGen)
        {
            // LOCALIZATION ANALYSIS
            // STEP 1 - This step remove reduces the number of localizations.
            // A1. If a turtle only options is a position, then no other symbol can produce that turtle
            // A2. If a turtle can only be produced in a single spot it must be produced in that spot
            // Example:  +: X(4) +(5) <---- remove this
            //           +: +(5)   <---- because this must the localization
            // B1. A symbol cannot be localized to a position if the next position does not have a localization equal or greater than the current symbol
            // Example: Sn   : 4,5,6 <---- remove the 6
            //          Sn+1 : 4,5
            // then Sn cannot be localized to symbol 6
            // B2. A symbol cannot be localized to a position if the previous position does not have a localization equal or greater than the current symbol
            // Example: Sn   : 5,6
            //          Sn+1 : 4,5,6 <--- remove the 4
            // C1. No symbol can be localized after the last localization of the previous symbol
            // C2. No symbol can be localized before the first localization of the next symbol

            // STEP 2 - these steps should finalize the localization settings, i.e. converting 1s to 2s or 1s to 0s
            // A1. If a symbol has any value is locked then remove the remainder
            // Example: Sn: 4,5*,6  <---- remove the 4 and 6
            // A2. If a symbol has only a single precedessor set it to 2

            // Repeat Steps 1 & 2 until convergence

            // STEP 3 - these steps discovery facts about the L-system, such as fragments
            // A. if a set of symbols can only be produced by one symbol, then that set is a fragment
            // i. if the uniqueness is at the start of the production it is a head fragment
            // ii. if the uniqueness is at the end of the production it is a tail fragment
            // iii. if the uniqueness is at the middle of the production it is a mid fragment
            // iv. if the uniqueness is at the start and end of the production it is a complete fragment
            // B. Remove any fragment which could not be localized into a wake, mark as tabu

            // STEP 1 - This step remove reduces the number of localizations repeat until convergence
            bool change = false;

            do
            {
                change = false;

                // A1. If a turtle only options is a position, then no other symbol can produce that turtle
                // Example: +: 4
                // Example: +: 4,5
                // Example: +: 5,6  <--- if this is the only option for 6 then 6 must produce this, so remove 5
                for (Int32 iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
                {
                    // Do process for A1
                    if (this->model->alphabet->IsTurtle(this->model->evidence[iGen]->GetSymbolIndex(iPos1)))
                    {
                        Int32 count = 0;
                        Int32 idx = 0;
                        Int32 iPos2 = 0;
                        while ((count < 2) && (iPos2 < this->model->evidence[iGen + 1]->Length()))
                        {
                            if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked))
                            {
                                count++;
                                idx = iPos2;
                            }
                            iPos2++;
                        }

                        if (count == 1)
                        {
                            for (size_t iPos3 = 0; iPos3 < this->model->evidence[iGen]->Length(); iPos3++)
                            {
                                if ((this->MAO->localization[iGen][idx, iPos3] == MasterAnalysisObject::cLocalization_StrongBTF) && (iPos1 != iPos3))
                                {
                                    this->MAO->SetLocalization(iGen, idx, iPos3, MasterAnalysisObject::cLocalization_Never);
                                    change = true;
                                }
                                else if ((this->MAO->localization[iGen][idx, iPos3] == MasterAnalysisObject::cLocalization_Locked) && (iPos1 != iPos3))
                                {
                                    Console::WriteLine("Uh oh!");
                                }
                            }
                        }
                    }

                    // Do process for C1 & C2. Find the first and last occurance for each symbol
                    Int32 first = -1;
                    Int32 last = 0;
                    Int32 iPos2 = 0;
                    bool locked = false;

                    while ((!locked) && (iPos2 < this->model->evidence[iGen + 1]->Length()))
                    {
                        if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF) && (first == -1) && (!locked))
                        {
                            first = iPos2;
                        }

                        if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF) && (!locked))
                        {
                            last = iPos2;
                        }

                        if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
                        {
                            first = iPos2;
                            last = iPos2;
                            locked = true;
                        }
                        iPos2++;
                    }

                    // C1. No symbol can be localized after the last localization of the previous symbol
                    // Example:  Sn: 3,4 <--- if this is the last instance of 4
                    //           Sn+1: 3,5 <--- remove the 3
                    for (size_t iPos2 = last + 1; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
                    {
                        for (Int32 iPos3 = 0; iPos3 < Math::Max(0, iPos1 - 1); iPos3++)
                        {
                            this->MAO->SetLocalization(iGen, iPos2, iPos3, MasterAnalysisObject::cLocalization_Never);
                        }
                    }

                    // C2. No symbol can be localized before the first localization of the next symbol
                    // Example:  Sn: 3,5 <--- remove the 5
                    //           Sn+1: 3,4 <--- if this is the first instance of 4
                    for (size_t iPos2 = 0; iPos2 < Math::Max(0, first - 1); iPos2++)
                    {
                        for (size_t iPos3 = iPos1 + 1; iPos3 < this->model->evidence[iGen]->Length(); iPos3++)
                        {
                            this->MAO->SetLocalization(iGen, iPos2, iPos3, MasterAnalysisObject::cLocalization_Never);
                        }
                    }
                }

                for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
                {
                    // A2. If a turtle can only be produced by a turtle, then it must be produced by that turtle
                    if (this->model->alphabet->IsTurtle(this->model->evidence[iGen + 1]->GetSymbolIndex(iPos2)))
                    {
                        Int32 count = 0;
                        Int32 idx = 0;
                        Int32 iPos1 = 0;
                        while ((count < 2) && (iPos1 < this->model->evidence[iGen]->Length()))
                        {
                            if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked))
                            {
                                count++;
                                idx = iPos1;
                            }
                            iPos1++;
                        }

                        // if the turtle can only be produced by a single turtle then eliminate all other possibilities
                        if ((count == 1) && (this->model->alphabet->IsTurtle(this->model->evidence[iGen]->GetSymbolIndex(idx))))
                        {
                            for (size_t iPos3 = 0; iPos3 < this->model->evidence[iGen + 1]->Length(); iPos3++)
                            {
                                if ((this->MAO->localization[iGen][iPos3, idx] == MasterAnalysisObject::cLocalization_StrongBTF) && (iPos2 != iPos3))
                                {
                                    this->MAO->SetLocalization(iGen, iPos3, idx, MasterAnalysisObject::cLocalization_Never);
                                    change = true;
                                }
                                else if ((this->MAO->localization[iGen][iPos3, idx] == MasterAnalysisObject::cLocalization_Locked) && (iPos2 != iPos3))
                                {
                                    Console::WriteLine("Uh oh!");
                                }
                            }
                        }
                    }

                    // B1. A symbol cannot be localized to a position if the next position does not have a localization equal or greater than the current symbol
                    Int32 largest = 0;
                    Int32 smallest = 999999;
                    for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
                    {
                        if ((iPos2 < this->model->evidence[iGen + 1]->Length() - 1) && ((this->MAO->localization[iGen][iPos2 + 1, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF) || (this->MAO->localization[iGen][iPos2 + 1, iPos1] == MasterAnalysisObject::cLocalization_Locked)) && (iPos1 > largest))
                        {
                            largest = iPos1;
                        }

                        if ((iPos2 > 0) && ((this->MAO->localization[iGen][iPos2 - 1, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF) || (this->MAO->localization[iGen][iPos2 - 1, iPos1] == MasterAnalysisObject::cLocalization_Locked)) && (iPos1 < smallest))
                        {
                            smallest = iPos1;
                        }
                    }

                    // Nothing larger than the largest in the next symbol can produce the current symbol
                    if (iPos2 < this->model->evidence[iGen + 1]->Length() - 1)
                    {
                        for (size_t iPos1 = largest + 1; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
                        {
                            if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF)
                            {
                                this->MAO->SetLocalization(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Never);
                                change = true;
                            }
                            else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
                            {
                                Console::WriteLine("Uh oh!");
                            }
                        }
                    }

                    // Nothing smaller than the smallest in the previous symbol can produce the current symbol
                    if (iPos2 > 0)
                    {
                        for (size_t iPos1 = 0; iPos1 < Math::Max(0, smallest - 1); iPos1++)
                        {
                            if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF)
                            {
                                this->MAO->SetLocalization(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Never);
                                change = true;
                            }
                            else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
                            {
                                Console::WriteLine("Uh oh!");
                            }
                        }
                    }

                    // STEP 2 - these steps should convert finalize the localization settings, i.e. converting 1s to 2s or 1s to 0s
                    // A1. If a symbol has any value is locked then remove the remainder
                    // A2. If a symbol has only a single precedessor set it to 2
                    Int32 count = 0;
                    Int32 idx = 0;
                    for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
                    {
                        if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
                        {
                            for (size_t iPos3 = 0; iPos3 < this->model->evidence[iGen]->Length(); iPos3++)
                            {
                                if ((iPos1 != iPos3) && (this->MAO->localization[iGen][iPos2, iPos3] != MasterAnalysisObject::cLocalization_Never))
                                {
                                    this->MAO->SetLocalization(iGen, iPos2, iPos3, MasterAnalysisObject::cLocalization_Never);
                                    change = true;
                                }
                            }
                        }
                        else if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked))
                        {
                            count++;
                            idx = iPos1;
                        }
                    }

                    if (count == 1)
                    {
                        this->MAO->SetLocalization(iGen, iPos2, idx, MasterAnalysisObject::cLocalization_Locked);
                        change = true;
                    }
                }
            } while (change);
        }
        """
        pass

    def compute_localization_findBTFcandidates_left_right(self):
        """
MaxFragmentCandidates^ LSIProblemV3::ComputeSymbolLocalization_FindBTFCandidates_LeftToRight(Int32 iGen, Int32 StartWake, Int32 EndWake, Fact^ F)
{
	MaxFragmentCandidates^ result = gcnew MaxFragmentCandidates();
	List<Int32>^ candidates = gcnew List<Int32>;
	List<Int32>^ btfIndex = gcnew List<Int32>;

	for (size_t iScan = StartWake; iScan <= EndWake; iScan++)
	{
		if (iScan < this->model->evidence[iGen + 1]->Length())
		{
			for (size_t iBTF = 0; iBTF < F->cache->Count; iBTF++)
			{
				String^ subwordMax = this->model->evidence[iGen + 1]->GetSymbols(iScan, F->cache[iBTF]->fragment->Length);
				if (subwordMax == F->cache[iBTF]->fragment)
				{
					if (candidates->Count == 0 || btfIndex[0] == iBTF)
					{
						candidates->Add(iScan);
						btfIndex->Add(iBTF);
					}
				}
			}
		}
	}

	result->candidates = candidates;
	result->fragmentIndex = btfIndex;

	return result;
}
        """
        pass


    def compute_localization_findBTFcandidates_right_left(self):
        """
        MaxFragmentCandidates^ LSIProblemV3::ComputeSymbolLocalization_FindBTFCandidates_RightToLeft(Int32 iGen, Int32 StartWake, Int32 EndWake, Fact^ F)
        {
            MaxFragmentCandidates^ result = gcnew MaxFragmentCandidates();
            List<Int32>^ candidates = gcnew List<Int32>;
            List<Int32>^ btfIndex = gcnew List<Int32>;

            for (size_t iScan = StartWake; iScan <= EndWake; iScan++)
            {
                if (iScan < this->model->evidence[iGen + 1]->Length())
                {
                    for (size_t iBTF = 0; iBTF < F->cache->Count; iBTF++)
                    {
                        Int32 start = iScan - F->cache[iBTF]->fragment->Length + 1;
                        if (start >= 0)
                        {
                            String^ subwordMax = this->model->evidence[iGen + 1]->GetSymbols(start, F->cache[iBTF]->fragment->Length);
                            if (subwordMax == F->cache[iBTF]->fragment)
                            {
                                if (candidates->Count == 0 || btfIndex[0] == iBTF)
                                {
                                    candidates->Add(iScan);
                                    btfIndex->Add(iBTF);
                                }
                            }
                        }
                    }
                }
            }

            result->candidates = candidates;
            result->fragmentIndex = btfIndex;

            return result;
        }
        """
        pass

    def compute_localization_find_max_fragment_left_right(self):
        """
        MaxFragmentCandidates^ LSIProblemV3::ComputeSymbolLocalization_FindMaxFragmentCandidates_LeftToRight(Int32 iGen, Int32 StartWake, Int32 EndWake, Fact^ F)
        {
            MaxFragmentCandidates^ result = gcnew MaxFragmentCandidates();
            List<Int32>^ candidates = gcnew List<Int32>;
            List<Int32>^ fragmentIndex = gcnew List<Int32>;

            for (size_t iScan = StartWake; iScan <= EndWake; iScan++)
            {
                if (iScan < this->model->evidence[iGen + 1]->Length())
                {
                    // Starting from iScan and scanning right, every right neighbour must be valid to at least one max fragments
                    for (size_t iFragment = 0; iFragment < F->max->Count; iFragment++)
                    {
                        String^ subwordMax = this->model->evidence[iGen + 1]->GetSymbols(iScan, F->max[iFragment]->fragment->Length);
                        if (subwordMax == F->max[iFragment]->fragment)
                        {
                            candidates->Add(iScan);
                            fragmentIndex->Add(iFragment);
                        }
                    }
                }
            }

            result->candidates = candidates;
            result->fragmentIndex = fragmentIndex;

            return result;
        }
        """
        pass

    def left_right_localization(self):
        """
        void LSIProblemV3::ComputeSymbolLocalization_LeftToRightLocalization(Int32 iGen)
        {
            Console::WriteLine("Left to Right Localization");
            Console::WriteLine("==========================");
            Int32 prevStart = 0;
            Int32 prevEnd = 0;
            bool prevIsTurtle = false;
            bool prevSingleCandidate = false;
            bool prevComplete = false;

            Console::WriteLine();

            for (size_t iPos = 0; iPos < this->model->evidence[iGen]->Length(); iPos++)
            {
        #if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
                Console::WriteLine(iPos + ": " + this->model->evidence[iGen]->GetSymbol(iPos) + " in wake from " + prevStart + " to " + prevEnd);
        #endif
                Int32 symbolIndex = this->model->evidence[iGen]->GetSymbolIndex(iPos);

                List<Int32>^ candidates = gcnew List<Int32>;

                if (this->model->alphabet->IsTurtle(symbolIndex))
                {
                    prevIsTurtle = true;
                    // All turtle symbols must be in the prev range or the right neighbour of the range
                    // Look to find all the places where the symbol matches
                    for (size_t iScan = prevStart; iScan <= prevEnd; iScan++)
                    {
                        if (iScan < this->model->evidence[iGen + 1]->Length()) // if the previous symbols range already extends to the end then don't scan outside the word
                        {
                            if ((symbolIndex == this->model->evidence[iGen + 1]->GetSymbolIndex(iScan)) && (this->ValidateRightNeighbourTurtle(this->model->evidence[iGen], this->model->evidence[iGen + 1], iPos + 1, iScan + 1)))
                            {
                                candidates->Add(iScan);
                            }
                        }
                    }

                    if (candidates->Count == 1)
                    {
                        prevSingleCandidate = true;
                        this->MAO->SetLocalization(iGen, candidates[0], iPos, MasterAnalysisObject::cLocalization_Locked);
                    }
                    else
                    {
                        prevSingleCandidate = false;
                        for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
                        {
                            this->MAO->SetLocalization(iGen, candidates[iCandidate], iPos, MasterAnalysisObject::cLocalization_Weak);
                        }
                    }

                    prevStart = candidates[0] + 1;
                    prevEnd = candidates[candidates->Count - 1] + 1;

                }
                else
                {
                    // if the prev symbol is a turtle, AND only had a single candidate
                    // then this create a head fragment for the current symbol
                    if ((prevIsTurtle) && (prevSingleCandidate))
                    {
                        prevSingleCandidate = true;
                        this->ComputeFragment_Position_HeadOnly(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevStart);
                    }

                    // Set the localization for the head fragments
                    Fact^ f = this->MAO->GetFact(iGen, this->model->evidence[iGen], iPos);
                    // Adjust the wake based on the WTW
                    Range^ wtw = this->model->evidence[iGen]->GetWTW(iPos);
                    if (prevStart < wtw->start)
                    {
                        prevStart = wtw->start;
                    }
                    if (prevEnd > wtw->end)
                    {
                        prevEnd = wtw->end;
                    }

                    List<Int32>^ candidatesBTF = gcnew List<Int32>;
                    List<Int32>^ candidatesHead = gcnew List<Int32>;
                    List<Int32>^ candidatesTail = gcnew List<Int32>;
                    List<Int32>^ candidatesMid = gcnew List<Int32>;
                    List<Int32>^ fragmentIndex = gcnew List<Int32>;
                    List<Int32>^ btfIndex = gcnew List<Int32>;
                    bool localizeHeadFragment = true;
                    bool localizeTailFragment = true;
                    bool localizeMaxFragment = true;
                    bool localizeMidFragment = true;
                    Int32 startWake = 99999;
                    Int32 endWake = 0;
                    Int32 startLocalizationLimit = 99999;
                    Int32 endLocalizationLimit = 0;
                    Int32 startWakeAbs = 99999;
                    Int32 endWakeAbs = 0;
                    prevIsTurtle = false;
                    FragmentSigned^ btf;

                    if (f->btf->Count == 1)
                    {
                        btf = f->btf[0];
                        this->model->evidence[iGen]->SetBTF(iPos, f->btf[0]);
                    }
                    else
                    {
                        btf = this->model->evidence[iGen]->GetBTF(iPos);
                    }

                    // if the head fragment is complete only localize the head fragment
                    if (f->head->min->isComplete)
                    {
                        localizeTailFragment = false;
                        localizeMidFragment = false;
                        localizeMaxFragment = false;
                    }

                    for (size_t iScan = prevStart; iScan <= prevEnd; iScan++)
                    {
                        if (iScan < this->model->evidence[iGen + 1]->Length())
                        {
                            String^ subwordMax = this->model->evidence[iGen + 1]->GetSymbols(iScan, btf->fragment->Length);
                            if (subwordMax == btf->fragment && (iScan >= wtw->start && iScan <= wtw->end))
                            {
                                candidatesBTF->Add(iScan);
                            }

                            if (f->head->min->fragment != nullptr)
                            {
                                String^ subwordHeadMin = this->model->evidence[iGen + 1]->GetSymbols(iScan, f->head->min->fragment->Length);
                                String^ subwordHeadMax = this->model->evidence[iGen + 1]->GetSymbols(iScan, f->head->max->fragment->Length);
                                if ((subwordHeadMin == f->head->min->fragment) && (subwordHeadMax == f->head->max->fragment))
                                {
                                    candidatesHead->Add(iScan);
                                }
                            }

                            if (f->tail->min->fragment != nullptr)
                            {
                                String^ subwordTailMax = this->model->evidence[iGen + 1]->GetSymbols(iScan, f->tail->max->fragment->Length);
                                String^ subwordTailMin = subwordTailMax->Substring(subwordTailMax->Length - f->tail->min->fragment->Length, f->tail->min->fragment->Length);
                                if ((subwordTailMin == f->tail->min->fragment) && (subwordTailMax == f->tail->max->fragment))
                                {
                                    candidatesTail->Add(iScan);
                                }
                            }

                            if (f->mid->fragment != nullptr)
                            {
                                String^ subwordMid = this->model->evidence[iGen + 1]->GetSymbols(iScan, f->mid->fragment->Length);
                                if (subwordMid == f->mid->fragment)
                                {
                                    candidatesMid->Add(iScan);
                                }
                            }
                        }
                    }

        #if _PHASE3_COMPUTE_LOCALIZATION_ >= 2
                    Console::Write("Head Fragment:");
                    for (size_t iCandidate = 0; iCandidate < candidatesHead->Count; iCandidate++)
                    {
                        Console::Write(candidatesHead[iCandidate] + " ");
                    }
                    Console::WriteLine();

                    Console::Write("Mid Fragment:");
                    for (size_t iCandidate = 0; iCandidate < candidatesMid->Count; iCandidate++)
                    {
                        Console::Write(candidatesMid[iCandidate] + " ");
                    }
                    Console::WriteLine();

                    Console::Write("Tail Fragment:");
                    for (size_t iCandidate = 0; iCandidate < candidatesTail->Count; iCandidate++)
                    {
                        Console::Write(candidatesTail[iCandidate] + " ");
                    }
                    Console::WriteLine();

                    Console::Write("Max Fragment:");
                    for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
                    {
                        Console::Write(candidates[iCandidate] + " ");
                    }
                    Console::WriteLine();
        #endif
                    // If not BTF fragment could be placed in the wake, then create a new BTF and localize it
                    if (candidatesBTF->Count == 0)
                    {
                        Fragment^ toCache;
                        Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + btf->fragment + " cannot be localized in wake " + this->model->evidence[iGen + 1]->GetSymbolsFromPos(prevStart, prevEnd));

                        // A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
                        // -- if this fails then it means the BTF comes from an instance with a non-compatible signature
                        toCache = this->ComputeBTF_LocalizationCompatability_LeftToRight(btf, this->model->evidence[iGen + 1], prevStart, prevEnd);

                        //// A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
                        //// -- if this fails then it means the BTF comes from an instance with a non-compatible signature
                        //Int32 iBTF = 0;
                        //bool btfFound = false;
                        //do
                        //{
                        //	btf = this->ComputeBTF_LocalizationCompatability_LeftToRight(f->btf[iBTF], this->model->evidence[iGen + 1], prevStart, prevEnd);
                        //	if (btf->fragment != nullptr)
                        //	{
                        //		btfFound = true;
                        //		Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by localization compatibility BTF " + btf->fragment);
                        //	}
                        //	else
                        //	{
                        //		Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + f->btf[iBTF]->fragment + " is not locally compatible.");
                        //	}
                        //	iBTF++;
                        //} while (!btfFound && iBTF < f->btf->Count);

                        ////// B. Create a BTF by considering the max fragments. A BTF is formed from the start of the wake to the end of the next wake.
                        ////if (btf->fragment == nullptr && candidates->Count > 0)
                        ////{
                        ////	Int32 btfStart = prevStart;
                        ////	Int32 btfEnd = 0;
                        ////	for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
                        ////	{
                        ////		if (btfEnd < candidates[iCandidate] + f->max[fragmentIndex[iCandidate]]->fragment->Length)
                        ////		{
                        ////			btfEnd = Math::Min(this->model->evidence[iGen + 1]->Length()-1, candidates[iCandidate] + f->max[fragmentIndex[iCandidate]]->fragment->Length);
                        ////		}
                        ////	}
                        ////	btf = this->MAO->CreateFragment(this->model->evidence[iGen + 1]->GetSymbolsFromPos(btfStart, btfEnd), false, true);
                        ////	Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found from max fragments BTF " + btf->fragment);
                        ////}

                        //// C. Create a BTF using the reserve algorithm
                        //if (btf->fragment == nullptr)
                        //{
                        //	btf = this->ComputeFragment_Position_BTFOnly_LeftToRight(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevStart, prevEnd);
                        //	Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by position reserve BTF " + btf->fragment);
                        //}

                        f->cache->Add(this->MAO->CreateBTF(toCache, btf->leftSignature, btf->rightSignature));
                        this->MAO->SetFact_BTFOnly_Update(btf, f->cache[f->cache->Count - 1], f);
                        Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by localization compatibility BTF " + toCache->fragment);
                        candidatesBTF = this->ComputeSymbolLocalization_MaxFragment_LeftToRight(btf, this->model->evidence[iGen + 1], prevStart, prevEnd);
                    }

                    for (size_t iCandidate = 0; iCandidate < candidatesBTF->Count; iCandidate++)
                    {
                        Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + btf->fragment + " @ " + candidatesBTF[iCandidate] + ".." + (candidatesBTF[iCandidate] + btf->fragment->Length - 1));
                        Console::WriteLine("Finding superstring candidates");
                        for (size_t iScan = prevStart; iScan <= prevEnd; iScan++)
                        {
                            if (iScan < this->model->evidence[iGen + 1]->Length())
                            {
                                for (size_t iFragment = 0; iFragment < f->max->Count; iFragment++)
                                {
                                    // Signature must match BTF or be blank
                                    bool signatureMatch = btf->leftSignature == f->max[iFragment]->leftSignature && btf->rightSignature == f->max[iFragment]->rightSignature;

                                    if (((f->max[iFragment]->leftSignature == "" && f->max[iFragment]->rightSignature == "")) || signatureMatch)
                                    {
                                        String^ subwordMax = this->model->evidence[iGen + 1]->GetSymbols(iScan, f->max[iFragment]->fragment->Length);
                                        if (subwordMax == f->max[iFragment]->fragment)
                                        {
                                            candidates->Add(iScan);
                                            fragmentIndex->Add(iFragment);
                                        }
                                    }
                                }
                            }
                        }

                        if (candidatesBTF[iCandidate] + f->length->min < startWakeAbs)
                        {
                            startWakeAbs = candidatesBTF[iCandidate] + f->length->min;
                        }
                        if (candidatesBTF[iCandidate] < startLocalizationLimit)
                        {
                            startLocalizationLimit = candidatesBTF[iCandidate];
                        }

                        if (candidatesBTF[iCandidate] + btf->fragment->Length > endWakeAbs)
                        {
                            endWakeAbs = candidatesBTF[iCandidate] + btf->fragment->Length;
                        }
                        if (candidatesBTF[iCandidate] + btf->fragment->Length - 1 > endLocalizationLimit)
                        {
                            endLocalizationLimit = candidatesBTF[iCandidate] + btf->fragment->Length - 1;
                        }

                        for (size_t iLength = 0; iLength < btf->fragment->Length; iLength++)
                        {
                            this->MAO->SetLocalization(iGen, candidatesBTF[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_WeakBTF);
                            // if there are no max fragments localilzed then upgrade to weak localization
                            if (candidates->Count == 0)
                            {
                                this->MAO->SetLocalization(iGen, candidatesBTF[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_Weak);
                            }
                        }
                    }

                    startLocalizationLimit = Math::Max(prevStart, startLocalizationLimit);
                    endLocalizationLimit = Math::Min(this->model->evidence[iGen + 1]->Length() - 1, Math::Min(prevEnd + f->length->max - 1, endLocalizationLimit));

                    Console::WriteLine("Absolute localization limit is " + startLocalizationLimit + " / " + endLocalizationLimit);

                    //// If no fragment could be placed in the wake, then
                    //// 1. tabu all of the current max fragments
                    //// 2. construct a new max fragment from the wake and add it as a candidate
                    //if ((candidates->Count == 0) && (candidatesHead->Count == 0) && (candidatesTail->Count == 0))
                    //{
                    //	List<Fragment^>^ toRemove = gcnew List<Fragment^>;
                    //	for (size_t iFragment = 0; iFragment < f->max->Count; iFragment++)
                    //	{
                    //		toRemove->Add(f->max[iFragment]);
                    //	}

                    //	for (size_t iFragment = 0; iFragment < toRemove->Count; iFragment++)
                    //	{
                    //		this->MAO->RemoveFact_MaxFragmentOnly(f, toRemove[iFragment], true);
                    //	}

                    //	Range^ r = this->ComputeFragment_Wake_LeftToRight(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevStart, prevEnd);
                    //	MaxFragmentCandidates^ x = this->ComputeSymbolLocalization_FindMaxFragmentCandidates_LeftToRight(iGen, prevStart, prevEnd, f);
                    //	candidates = x->candidates;
                    //	fragmentIndex = x->fragmentIndex;
                    //}

                    if ((localizeHeadFragment) && (candidatesHead->Count > 0))
                    {
                        localizeMaxFragment = false; // if the head fragment gets set then there is no need to localize the max fragment
                        for (size_t iCandidate = 0; iCandidate < candidatesHead->Count; iCandidate++)
                        {
                            Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " Head Fragment " + f->head->min->fragment + " / " + f->head->max->fragment + " @ " + candidatesHead[iCandidate]);

                            if (candidatesHead[iCandidate] + f->length->min < startWake)
                            {
                                startWake = candidatesHead[iCandidate] + f->length->min;
                            }
                            if (candidatesHead[iCandidate] + f->head->max->fragment->Length > endWake)
                            {
                                endWake = candidatesHead[iCandidate] + f->head->max->fragment->Length;
                            }

                            for (size_t iLength = 0; iLength < f->head->max->fragment->Length; iLength++)
                            {
                                if (candidatesHead[iCandidate] + iLength >= startLocalizationLimit && candidatesHead[iCandidate] + iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidatesHead[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_Weak);
                                }
                            }
                            for (size_t iLength = 0; iLength < f->head->min->fragment->Length; iLength++)
                            {
                                if (candidatesHead->Count == 1 && candidatesHead[iCandidate] + iLength >= startLocalizationLimit && candidatesHead[iCandidate] + iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidatesHead[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_Locked);
                                }
                                else if (candidatesHead[iCandidate] + iLength >= startLocalizationLimit && candidatesHead[iCandidate] + iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidatesHead[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_Weak);
                                }
                            }
                        }
                    }

                    // Set the localization for the tail fragments
                    if ((localizeTailFragment) && (candidatesTail->Count > 0))
                    {
                        localizeMaxFragment = false; // if the head fragment gets set then there is no need to localize the max fragment
                        for (size_t iCandidate = 0; iCandidate < candidatesTail->Count; iCandidate++)
                        {
                            Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " Tail Fragment " + f->tail->min->fragment + " / " + f->tail->max->fragment + " @ " + candidatesTail[iCandidate]);

                            if (candidatesTail[iCandidate] + f->length->min < startWake)
                            {
                                startWake = candidatesTail[iCandidate] + f->length->min;
                            }
                            if (candidatesTail[iCandidate] + f->tail->max->fragment->Length > endWake)
                            {
                                endWake = candidatesTail[iCandidate] + f->tail->max->fragment->Length;
                            }

                            for (size_t iLength = 0; iLength < f->tail->max->fragment->Length; iLength++)
                            {
                                if (candidatesTail[iCandidate] + iLength >= startLocalizationLimit && candidatesTail[iCandidate] + iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidatesTail[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_Weak);
                                }
                            }

                            for (size_t iLength = 1; iLength <= f->tail->min->fragment->Length; iLength++)
                            {
                                if (candidatesTail->Count > 1 && candidatesTail[iCandidate] + f->tail->max->fragment->Length - iLength >= startLocalizationLimit && candidatesTail[iCandidate] + f->tail->max->fragment->Length - iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidatesTail[iCandidate] + f->tail->max->fragment->Length - iLength, iPos, MasterAnalysisObject::cLocalization_Weak);
                                }
                                else if (candidatesTail[iCandidate] + f->tail->max->fragment->Length - iLength >= startLocalizationLimit && candidatesTail[iCandidate] + f->tail->max->fragment->Length - iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidatesTail[iCandidate] + f->tail->max->fragment->Length - iLength, iPos, MasterAnalysisObject::cLocalization_Locked);
                                }
                            }
                        }
                    }

                    // Set the localization for the max fragments
                    if (localizeMaxFragment)
                    {
                        for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
                        {
                            Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " Max Fragment " + f->max[fragmentIndex[iCandidate]]->fragment + " @ " + candidates[iCandidate] + ".." + (candidates[iCandidate] + f->max[fragmentIndex[iCandidate]]->fragment->Length - 1));
                            if (candidates[iCandidate] + f->length->min < startWake)
                            {
                                startWake = candidates[iCandidate] + f->length->min;
                            }
                            if (candidates[iCandidate] + f->max[fragmentIndex[iCandidate]]->fragment->Length > endWake)
                            {
                                endWake = candidates[iCandidate] + f->max[fragmentIndex[iCandidate]]->fragment->Length;
                            }

                            for (size_t iLength = 0; iLength < f->max[fragmentIndex[iCandidate]]->fragment->Length; iLength++)
                            {
                                if (candidates[iCandidate] + iLength >= startLocalizationLimit && candidates[iCandidate] + iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidates[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_Weak);
                                }
                            }
                        }
                    }

                    // Set the localization for the mid fragments
                    if ((localizeMidFragment) && (candidatesMid->Count > 0))
                    {
                        for (size_t iCandidate = 0; iCandidate < candidatesMid->Count; iCandidate++)
                        {
                            Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " Mid Fragments " + f->mid->fragment + " @ " + candidatesMid[iCandidate]);
                            for (size_t iLength = 0; iLength < f->mid->fragment->Length; iLength++)
                            {
                                if (candidatesMid->Count > 1 && candidatesMid[iCandidate] + iLength >= startLocalizationLimit && candidatesMid[iCandidate] + iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidatesMid[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_Weak);
                                }
                                else if (candidatesMid[iCandidate] + iLength >= startLocalizationLimit && candidatesMid[iCandidate] + iLength <= endLocalizationLimit)
                                {
                                    this->MAO->SetLocalization(iGen, candidatesMid[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_Locked);
                                }
                            }
                        }
                    }

        //			// Any max fragment that could not be placed in the wake is tabu
        //			List<Fragment^>^ toRemove = gcnew List<Fragment^>;
        //			for (size_t iFragment = 0; iFragment < f->max->Count; iFragment++)
        //			{
        //				if (!fragmentIndex->Contains(iFragment))
        //				{
        //#if _PHASE3_COMPUTE_LOCALIZATION_ >= 2
        //					Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " max fragment " + f->max[iFragment]->fragment + " is tabu");
        //#endif
        //					toRemove->Add(f->max[iFragment]);
        //					// remove any max fragment that could not be placed in the wake as false
        //				}
        //			}
        //			this->MAO->RemoveFact_MaxFragmentOnly(f, toRemove, true);

                    if ((startWakeAbs > startWake) || (startWake == 99999))
                    {
                        startWake = startWakeAbs;
                    }

                    if (startLocalizationLimit > startWake)
                    {
                        startWake = startLocalizationLimit;
                    }

                    if ((endWakeAbs < endWake) || (endWake == 0))
                    {
                        endWake = endWakeAbs;
                    }

                    if (endLocalizationLimit+1 < endWake)
                    {
                        endWake = endLocalizationLimit+1;
                    }

                    prevStart = startWake;
                    prevEnd = endWake;
                }
            }
        }
        """
        pass

    def left_right_localization_BTF_only(self):
        """
        void LSIProblemV3::ComputeSymbolLocalization_LeftToRightLocalization_BTFOnly(Int32 iGen)
        {
            Console::WriteLine("Left to Right Localization BTF Only");
            Console::WriteLine("===================================");
            Int32 prevStart = 0;
            Int32 prevEnd = 0;
            bool prevIsTurtle = false;
            bool prevSingleCandidate = false;
            bool prevComplete = false;

            Console::WriteLine();

            for (size_t iPos = 0; iPos < this->model->evidence[iGen]->Length(); iPos++)
            {
        #if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
                Console::WriteLine(iPos + ": " + this->model->evidence[iGen]->GetSymbol(iPos) + " in wake from " + prevStart + " to " + prevEnd);
        #endif
                Int32 symbolIndex = this->model->evidence[iGen]->GetSymbolIndex(iPos);

                List<Int32>^ candidates = gcnew List<Int32>;

                if (this->model->alphabet->IsTurtle(symbolIndex))
                {
                    prevIsTurtle = true;
                    // All turtle symbols must be in the prev range or the right neighbour of the range
                    // Look to find all the places where the symbol matches
                    for (size_t iScan = prevStart; iScan <= prevEnd; iScan++)
                    {
                        if (iScan < this->model->evidence[iGen + 1]->Length()) // if the previous symbols range already extends to the end then don't scan outside the word
                        {
                            if ((symbolIndex == this->model->evidence[iGen + 1]->GetSymbolIndex(iScan)) && (this->ValidateRightNeighbourTurtle(this->model->evidence[iGen], this->model->evidence[iGen + 1], iPos + 1, iScan + 1)))
                            {
                                candidates->Add(iScan);
                            }
                        }
                    }

                    if (candidates->Count == 1)
                    {
                        prevSingleCandidate = true;
                        this->MAO->SetLocalization(iGen, candidates[0], iPos, MasterAnalysisObject::cLocalization_Locked);
                    }
                    else
                    {
                        prevSingleCandidate = false;
                        for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
                        {
                            this->MAO->SetLocalization(iGen, candidates[iCandidate], iPos, MasterAnalysisObject::cLocalization_Weak);
                        }
                    }

                    prevStart = candidates[0] + 1;
                    prevEnd = candidates[candidates->Count - 1] + 1;

                }
                else
                {
                    // Set the localization for the head fragments
                    Fact^ f = this->MAO->GetFact(iGen, this->model->evidence[iGen], iPos);
                    // Adjust the wake based on the WTW
                    Range^ wtw = this->model->evidence[iGen]->GetWTW(iPos);
                    if (prevStart < wtw->start)
                    {
                        prevStart = wtw->start;
                    }
                    if (prevEnd > wtw->end)
                    {
                        prevEnd = wtw->end;
                    }

                    List<Int32>^ candidatesBTF = gcnew List<Int32>;
                    Int32 startWake = 99999;
                    Int32 endWake = 0;
                    Int32 startLocalizationLimit = 99999;
                    Int32 endLocalizationLimit = 0;
                    prevIsTurtle = false;
                    FragmentSigned^ btf;

                    if (f->btf->Count == 1)
                    {
                        btf = f->btf[0];
                        this->model->evidence[iGen]->SetBTF(iPos, f->btf[0]);
                    }
                    else
                    {
                        btf = this->model->evidence[iGen]->GetBTF(iPos);
                    }

                    for (size_t iScan = prevStart; iScan <= prevEnd; iScan++)
                    {
                        if (iScan < this->model->evidence[iGen + 1]->Length())
                        {
                            String^ subword = this->model->evidence[iGen + 1]->GetSymbols(iScan, btf->fragment->Length);
                            if (subword == btf->fragment && (iScan >= wtw->start && iScan <= wtw->end))
                            {
                                candidatesBTF->Add(iScan);
                            }
                        }
                    }

                    // If not BTF fragment could be placed in the wake, then create a new BTF and localize it
                    if (candidatesBTF->Count == 0)
                    {
                        Fragment^ toCache;
                        Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + btf->fragment + " cannot be localized in wake " + this->model->evidence[iGen + 1]->GetSymbolsFromPos(prevStart, prevEnd));

                        // A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
                        // -- if this fails then it means the BTF comes from an instance with a non-compatible signature
                        Fragment^ tmp1 = this->ComputeBTF_LocalizationCompatability_LeftToRight(btf, this->model->evidence[iGen + 1], prevStart, prevEnd);
                        Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by localization compatibility BTF " + tmp1->fragment);

                        // B. Create a BTF by considering the max fragments. A BTF is formed from the start of the wake to the end of the next wake.
                        Int32 btfStart = prevStart;
                        Int32 btfEnd = prevEnd + f->length->max;
                        Fragment^ tmp2 = this->MAO->CreateFragment(this->model->evidence[iGen + 1]->GetSymbolsFromPos(btfStart, btfEnd), false, true);
                        Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by wake + max length BTF " + tmp2->fragment);

                        //// C. Create a BTF using the reserve algorithm
                        //Fragment^ tmp3 = this->ComputeFragment_Position_BTFOnly_LeftToRight(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevStart, prevEnd);
                        //Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by position reserve BTF " + btf->fragment);

                        if (tmp1->fragment == nullptr || tmp2->fragment->Length < tmp1->fragment->Length)
                        {
                            toCache = tmp2;
                        }
                        else
                        {
                            toCache = tmp1;
                        }

                        f->cache->Add(this->MAO->CreateBTF(toCache, btf->leftSignature, btf->rightSignature));
                        this->MAO->SetFact_BTFOnly_Update(btf, f->cache[f->cache->Count - 1], f);
                        candidatesBTF = this->ComputeSymbolLocalization_MaxFragment_LeftToRight(btf, this->model->evidence[iGen + 1], prevStart, prevEnd);
                    }

                    for (size_t iCandidate = 0; iCandidate < candidatesBTF->Count; iCandidate++)
                    {
                        Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + btf->fragment + " @ " + candidatesBTF[iCandidate] + ".." + (candidatesBTF[iCandidate] + btf->fragment->Length - 1));

                        if (candidatesBTF[iCandidate] + f->length->min < startWake)
                        {
                            startWake = candidatesBTF[iCandidate] + f->length->min;
                        }
                        if (candidatesBTF[iCandidate] < startLocalizationLimit)
                        {
                            startLocalizationLimit = candidatesBTF[iCandidate];
                        }

                        if (candidatesBTF[iCandidate] + btf->fragment->Length > endWake)
                        {
                            endWake = candidatesBTF[iCandidate] + btf->fragment->Length;
                        }
                        if (candidatesBTF[iCandidate] + btf->fragment->Length - 1 > endLocalizationLimit)
                        {
                            endLocalizationLimit = candidatesBTF[iCandidate] + btf->fragment->Length - 1;
                        }

                        for (size_t iLength = 0; iLength < btf->fragment->Length; iLength++)
                        {
                            this->MAO->SetLocalization(iGen, candidatesBTF[iCandidate] + iLength, iPos, MasterAnalysisObject::cLocalization_WeakBTF);
                        }
                    }

                    startLocalizationLimit = Math::Max(prevStart, startLocalizationLimit);
                    endLocalizationLimit = Math::Min(this->model->evidence[iGen + 1]->Length() - 1, Math::Min(prevEnd + f->length->max - 1, endLocalizationLimit));

                    Console::WriteLine("Absolute localization limit is " + startLocalizationLimit + " / " + endLocalizationLimit);

                    if (startLocalizationLimit > startWake)
                    {
                        startWake = startLocalizationLimit;
                    }

                    if (endLocalizationLimit + 1 < endWake)
                    {
                        endWake = endLocalizationLimit + 1;
                    }

                    prevStart = startWake;
                    prevEnd = endWake;

                    if (iGen >= 999)
                    {
                        Console::ReadLine();
                    }
                }
            }
        }
        """
        pass

    def right_left_localization(self):
        """
void LSIProblemV3::ComputeSymbolLocalization_RightToLeftLocalization(Int32 iGen)
{
	Console::WriteLine("Right to Left Localization");
	Console::WriteLine("==========================");
	Int32 prevStart = this->model->evidence[iGen + 1]->Length() - 1;
	Int32 prevEnd = this->model->evidence[iGen + 1]->Length() - 1;
	bool prevIsTurtle = false;
	bool prevSingleCandidate = false;
	bool prevComplete = false;

	Console::WriteLine();
	//this->MAO->localization[iGen] = gcnew array<Byte, 2>(this->model->evidence[iGen + 1]->Length(), this->model->evidence[iGen]->Length());

	for (Int16 iPos = this->model->evidence[iGen]->Length()-1; iPos >= 0; --iPos)
	{
#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
		Console::WriteLine(iPos + ": " + this->model->evidence[iGen]->GetSymbol(iPos) + " in wake from " + prevStart + " to " + prevEnd);
#endif
		Int32 symbolIndex = this->model->evidence[iGen]->GetSymbolIndex(iPos);

		List<Int32>^ candidates = gcnew List<Int32>;

		if (this->model->alphabet->IsTurtle(symbolIndex))
		{
			prevIsTurtle = true;
			// All turtle symbols must be in the prev range or the right neighbour of the range
			// Look to find all the places where the symbol matches
			for (Int16 iScan = prevStart; iScan >= prevEnd; --iScan)
			{
				if (iScan < this->model->evidence[iGen + 1]->Length()) // if the previous symbols range already extends to the end then don't scan outside the word
				{
					if ((symbolIndex == this->model->evidence[iGen + 1]->GetSymbolIndex(iScan)) && (this->ValidateLeftNeighbourTurtle(this->model->evidence[iGen], this->model->evidence[iGen + 1], iPos - 1, iScan - 1)))
					{
						candidates->Add(iScan);
					}
				}
			}

			if (candidates->Count == 1)
			{
				prevSingleCandidate = true;
				this->MAO->SetLocalization(iGen, candidates[0], iPos, MasterAnalysisObject::cLocalization_Locked);
				//this->MAO->localization[iGen][candidates[0], iPos] = cLocalization_Locked;
			}
			else
			{
				prevSingleCandidate = false;
				for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
				{
					// Upgrade the setting from weak to strong
					this->MAO->SetLocalization(iGen, candidates[iCandidate], iPos, MasterAnalysisObject::cLocalization_Strong);
					//if (this->MAO->localization[iGen][candidates[iCandidate], iPos] == cLocalization_Weak)
					//{
					//	this->MAO->localization[iGen][candidates[iCandidate], iPos] = cLocalization_Strong;
					//}
				}
			}

			prevStart = candidates[0] - 1;
			prevEnd = candidates[candidates->Count - 1] - 1;

		}
		else
		{
			// if the prev symbol is a turtle, AND only had a single candidate
			// then this create a head fragment for the current symbol
			if ((prevIsTurtle) && (prevSingleCandidate))
			{
				prevSingleCandidate = true;
				this->ComputeFragment_Position_TailOnly(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevStart);
			}

			// Set the localization for the head fragments
			Fact^ f = this->MAO->GetFact(iGen, this->model->evidence[iGen], iPos);
			// Adjust the wake based on the WTW
			Range^ wtw = this->model->evidence[iGen]->GetWTW(iPos);
			if (prevStart < wtw->start)
			{
				prevStart = wtw->start;
			}
			if (prevEnd > wtw->end)
			{
				prevEnd = wtw->end;
			}


			List<Int32>^ candidatesBTF = gcnew List<Int32>;
			List<Int32>^ candidatesHead = gcnew List<Int32>;
			List<Int32>^ candidatesTail = gcnew List<Int32>;
			List<Int32>^ candidatesMid = gcnew List<Int32>;
			List<Int32>^ fragmentIndex = gcnew List<Int32>;
			List<Int32>^ btfIndex = gcnew List<Int32>;
			bool localizeHeadFragment = true;
			bool localizeTailFragment = true;
			bool localizeMaxFragment = true;
			bool localizeMidFragment = true;
			Int32 startWake = 0;
			Int32 endWake = 99999;
			Int32 startLocalizationLimit = 0;
			Int32 endLocalizationLimit = 99999;
			Int32 startWakeAbs = 0;
			Int32 endWakeAbs = 99999;
			prevIsTurtle = false;
			FragmentSigned^ btf;

			if (f->btf->Count == 1)
			{
				btf = f->btf[0];
				this->model->evidence[iGen]->SetBTF(iPos, f->btf[0]);
			}
			else
			{
				btf = this->model->evidence[iGen]->GetBTF(iPos);
			}

			// if the head fragment is complete only localize the head fragment
			if (f->head->min->isComplete)
			{
				localizeTailFragment = false;
				localizeMidFragment = false;
				localizeMaxFragment = false;
			}

			for (Int16 iScan = prevStart; iScan >= prevEnd; --iScan)
			{
				if (iScan < this->model->evidence[iGen + 1]->Length())
				{
					Int32 start = iScan - btf->fragment->Length + 1;
					Int32 end = start + btf->fragment->Length;
					if (start >= 0)
					{
						String^ subwordMax = this->model->evidence[iGen + 1]->GetSymbols(start, btf->fragment->Length);
						if (subwordMax == btf->fragment && (iScan <= wtw->end && iScan >= wtw->start))
						{
							candidatesBTF->Add(iScan);
						}
					}

					if (f->head->min->fragment != nullptr)
					{
						Int32 start = iScan - f->head->max->fragment->Length + 1;
						if (start >= 0)
						{
							String^ subwordHeadMin = this->model->evidence[iGen + 1]->GetSymbols(start, f->head->min->fragment->Length);
							String^ subwordHeadMax = this->model->evidence[iGen + 1]->GetSymbols(start, f->head->max->fragment->Length);
							if ((subwordHeadMin == f->head->min->fragment) && (subwordHeadMax == f->head->max->fragment))
							{
								candidatesHead->Add(iScan);
							}
						}
					}

					if (f->tail->min->fragment != nullptr)
					{
						Int32 start = iScan - f->tail->max->fragment->Length + 1;
						if (start >= 0)
						{
							String^ subwordTailMin = this->model->evidence[iGen + 1]->GetSymbols(iScan - f->tail->min->fragment->Length + 1, f->tail->min->fragment->Length);
							String^ subwordTailMax = this->model->evidence[iGen + 1]->GetSymbols(start, f->tail->max->fragment->Length);
							if ((subwordTailMin == f->tail->min->fragment) && (subwordTailMax == f->tail->max->fragment))
							{
								candidatesTail->Add(iScan);
							}
						}
					}

					if (f->mid->fragment != nullptr)
					{
						Int32 start = iScan - f->mid->fragment->Length + 1;
						if (start >= 0)
						{
							String^ subwordMid = this->model->evidence[iGen + 1]->GetSymbols(start, f->mid->fragment->Length);
							if (subwordMid == f->mid->fragment)
							{
								candidatesMid->Add(iScan);
							}
						}
					}
				}
			}

#if _PHASE3_COMPUTE_LOCALIZATION_ >= 2
			Console::Write("Head Fragment:");
			for (size_t iCandidate = 0; iCandidate < candidatesHead->Count; iCandidate++)
			{
				Console::Write(candidatesHead[iCandidate] + " ");
			}
			Console::WriteLine();

			Console::Write("Mid Fragment:");
			for (size_t iCandidate = 0; iCandidate < candidatesMid->Count; iCandidate++)
			{
				Console::Write(candidatesMid[iCandidate] + " ");
			}
			Console::WriteLine();

			Console::Write("Tail Fragment:");
			for (size_t iCandidate = 0; iCandidate < candidatesTail->Count; iCandidate++)
			{
				Console::Write(candidatesTail[iCandidate] + " ");
			}
			Console::WriteLine();

			Console::Write("Max Fragment:");
			for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
			{
				Console::Write(candidates[iCandidate] + " ");
			}
			Console::WriteLine();
#endif
			// If no BTF could be placed in the wake, then create a new BTF and localize it
			// A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
			// -- if this fails then it means the BTF comes from an instance with a non-compatible signature
			// B. Create a BTF by considering the max fragments. A BTF is formed from the start of the wake to the end of the next wake.
			// C. Create a BTF using the reserve algorithm
			if (candidatesBTF->Count == 0)
			{
				Fragment^ toCache;
				Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + btf->fragment + " cannot be localized in wake " + this->model->evidence[iGen + 1]->GetSymbolsFromPos(prevEnd, prevStart));

				// A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
				// -- if this fails then it means the BTF comes from an instance with a non-compatible signature
				toCache = this->ComputeBTF_LocalizationCompatability_RightToLeft(btf, this->model->evidence[iGen + 1], prevEnd, prevStart);

				//// A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
				//// -- if this fails then it means the BTF comes from an instance with a non-compatible signature
				//Int32 iBTF = 0;
				//bool btfFound = false;
				//do
				//{
				//	btf = this->ComputeBTF_LocalizationCompatability_RightToLeft(f->btf[iBTF], this->model->evidence[iGen + 1], prevEnd, prevStart);
				//	if (btf->fragment != nullptr)
				//	{
				//		btfFound = true;
				//		Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by localization compatibility BTF " + btf->fragment);
				//	}
				//	else
				//	{
				//		Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + f->btf[iBTF]->fragment + " is not locally compatible.");
				//	}
				//	iBTF++;
				//} while (!btfFound && iBTF < f->btf->Count);

				//// B. Create a BTF by considering the max fragments. A BTF is formed from the start of the wake to the end of the next wake.
				//if (btf->fragment == nullptr && candidates->Count > 0)
				//{
				//	Int32 btfStart = 99999;
				//	Int32 btfEnd = prevStart;
				//	for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
				//	{
				//		if (btfStart > candidates[iCandidate] - f->max[fragmentIndex[iCandidate]]->fragment->Length)
				//		{
				//			btfStart = Math::Max(0, candidates[iCandidate] - f->max[fragmentIndex[iCandidate]]->fragment->Length);
				//		}
				//	}
				//	btf = this->MAO->CreateFragment(this->model->evidence[iGen + 1]->GetSymbolsFromPos(btfStart, btfEnd),false,true);
				//	Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found from max fragments BTF " + btf->fragment);
				//}

				// C. Create a BTF using the reserve algorithm
				//if (toCache->fragment == nullptr)
				//{
				//	toCache = this->ComputeFragment_Position_BTFOnly_RightToLeft(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevEnd,prevStart);
				//	Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by position reserve BTF " + toCache->fragment);
				//}

				f->cache->Add(this->MAO->CreateBTF(toCache, btf->leftSignature, btf->rightSignature));
				btf->fragment = toCache->fragment;
				Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by localization compatibility BTF " + btf->fragment);
				candidatesBTF = this->ComputeSymbolLocalization_MaxFragment_RightToLeft(btf, this->model->evidence[iGen + 1], prevEnd, prevStart);
			}

			for (size_t iCandidate = 0; iCandidate < candidatesBTF->Count; iCandidate++)
			{
				Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + btf->fragment + " @ " + candidatesBTF[iCandidate] + ".." + (1 + candidatesBTF[iCandidate] - btf->fragment->Length));
				Console::WriteLine("Finding superstring localizations");

				// Starting from iScan and scanning right, every right neighbour must be valid to at least one max fragments
				for (Int16 iScan = prevStart; iScan >= prevEnd; --iScan)
				{
					if (iScan < this->model->evidence[iGen + 1]->Length())
					{
						for (size_t iFragment = 0; iFragment < f->max->Count; iFragment++)
						{
							Int32 start = iScan - f->max[iFragment]->fragment->Length + 1;
							bool signatureMatch = btf->leftSignature == f->max[iFragment]->leftSignature && btf->rightSignature == f->max[iFragment]->rightSignature;

							if ((start >= 0) && ((f->max[iFragment]->leftSignature == "" && f->max[iFragment]->rightSignature == "") || signatureMatch))
							{
								String^ subwordMax = this->model->evidence[iGen + 1]->GetSymbols(start, f->max[iFragment]->fragment->Length);
								if (subwordMax == f->max[iFragment]->fragment)
								{
									candidates->Add(iScan);
									fragmentIndex->Add(iFragment);
								}
							}
						}
					}
				}


				if (candidatesBTF[iCandidate] - f->length->min > startWakeAbs)
				{
					startWakeAbs = candidatesBTF[iCandidate] - f->length->min;
				}
				if (candidatesBTF[iCandidate] > startLocalizationLimit)
				{
					startLocalizationLimit = candidatesBTF[iCandidate];
				}

				if (candidatesBTF[iCandidate] - btf->fragment->Length < endWakeAbs)
				{
					endWakeAbs = candidatesBTF[iCandidate] - btf->fragment->Length;
				}
				if (candidatesBTF[iCandidate] - btf->fragment->Length + 1 < endLocalizationLimit)
				{
					endLocalizationLimit = candidatesBTF[iCandidate] - btf->fragment->Length + 1;
				}

				for (size_t iLength = 0; iLength < btf->fragment->Length; iLength++)
				{
					this->MAO->SetLocalization(iGen, candidatesBTF[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_StrongBTF);
					if (candidates->Count == 0)
					{
						this->MAO->SetLocalization(iGen, candidatesBTF[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_Strong);
					}
				}
			}

			startLocalizationLimit = Math::Min(prevStart, startLocalizationLimit);
			endLocalizationLimit = Math::Max(0, Math::Max(prevEnd - f->length->max + 1, endLocalizationLimit));

			Console::WriteLine("Absolute localization limit is " + startLocalizationLimit + " / " + endLocalizationLimit);

			//// If no fragment could be placed in the wake, then
			//// 1. tabu all of the current max fragments
			//// 2. construct a new max fragment from the wake and add it as a candidate
			//if ((candidates->Count == 0) && (candidatesHead->Count == 0) && (candidatesTail->Count == 0))
			//{
			//	List<Fragment^>^ toRemove = gcnew List<Fragment^>;
			//	for (size_t iFragment = 0; iFragment < f->max->Count; iFragment++)
			//	{
			//		toRemove->Add(f->max[iFragment]);
			//	}

			//	for (size_t iFragment = 0; iFragment < toRemove->Count; iFragment++)
			//	{
			//		this->MAO->RemoveFact_MaxFragmentOnly(f, toRemove[iFragment], true);
			//	}

			//	Range^ r = this->ComputeFragment_Wake_RightToLeft(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevStart, prevEnd);
			//	MaxFragmentCandidates^ x = this->ComputeSymbolLocalization_FindMaxFragmentCandidates_RightToLeft(iGen, prevEnd, prevStart, f);
			//	candidates = x->candidates;
			//	fragmentIndex = x->fragmentIndex;
			//}

			if ((localizeHeadFragment) && (candidatesHead->Count > 0))
			{
				localizeMaxFragment = false; // if the head fragment gets set then there is no need to localize the max fragment
				for (size_t iCandidate = 0; iCandidate < candidatesHead->Count; iCandidate++)
				{
					Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " Head Fragment " + f->head->min->fragment + " / " + f->head->max->fragment + " @ " + candidatesHead[iCandidate]);

					if (candidatesHead[iCandidate] - f->length->min > startWake)
					{
						startWake = Math::Max(0,candidatesHead[iCandidate] - f->length->min);
					}
					if (candidatesHead[iCandidate] - f->head->max->fragment->Length < endWake)
					{
						endWake = Math::Max(0, candidatesHead[iCandidate] - f->head->max->fragment->Length); // no +1 because we want to include the NEXT symbol
					}

					for (size_t iLength = 0; iLength < f->head->max->fragment->Length; iLength++)
					{
						if (candidatesHead[iCandidate] - iLength <= startLocalizationLimit && candidatesHead[iCandidate] - iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidatesHead[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_Strong);
						}
					}

					for (size_t iLength = 1; iLength <= f->head->min->fragment->Length; iLength++)
					{
						if (candidatesHead->Count == 1 && candidatesHead[iCandidate] - f->head->max->fragment->Length + iLength <= startLocalizationLimit && candidatesHead[iCandidate] - f->head->max->fragment->Length + iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidatesHead[iCandidate] - f->head->max->fragment->Length + iLength, iPos, MasterAnalysisObject::cLocalization_Locked);
						}
						else if (candidatesHead[iCandidate] - f->head->max->fragment->Length + iLength <= startLocalizationLimit && candidatesHead[iCandidate] - f->head->max->fragment->Length + iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidatesHead[iCandidate] - f->head->max->fragment->Length + iLength, iPos, MasterAnalysisObject::cLocalization_Strong);
						}
					}
				}
			}

			// Set the localization for the tail fragments
			if ((localizeTailFragment) && (candidatesTail->Count > 0))
			{
				localizeMaxFragment = false; // if the head fragment gets set then there is no need to localize the max fragment
				for (size_t iCandidate = 0; iCandidate < candidatesTail->Count; iCandidate++)
				{
					Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " Tail Fragment " + f->tail->min->fragment + " / " + f->tail->max->fragment + " @ " + candidatesTail[iCandidate]);

					if (candidatesTail[iCandidate] - f->length->min > startWake)
					{
						startWake = Math::Max(0, candidatesTail[iCandidate] - f->length->min);
					}
					if (candidatesTail[iCandidate] - f->tail->max->fragment->Length < endWake)
					{
						endWake = Math::Max(0, candidatesTail[iCandidate] - f->tail->max->fragment->Length); // no +1 because we want to include the NEXT symbol
					}

					for (size_t iLength = 0; iLength < f->tail->max->fragment->Length; iLength++)
					{
						if (candidatesTail[iCandidate] - iLength <= startLocalizationLimit && candidatesTail[iCandidate] - iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidatesTail[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_Strong);
						}
					}

					for (size_t iLength = 0; iLength < f->tail->min->fragment->Length; iLength++)
					{
						if (candidatesTail->Count == 1 && candidatesTail[iCandidate] - iLength <= startLocalizationLimit && candidatesTail[iCandidate] - iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidatesTail[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_Locked);
						}
						else if (candidatesTail[iCandidate] - iLength <= startLocalizationLimit && candidatesTail[iCandidate] - iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidatesTail[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_Strong);
						}
					}
				}
			}

			// Set the localization for the max fragments
			if (localizeMaxFragment)
			{
				for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
				{
					if (candidates[iCandidate] - f->length->min > startWake)
					{
						startWake = Math::Max(0, candidates[iCandidate] - f->length->min);
					}
					if (candidates[iCandidate] - f->max[fragmentIndex[iCandidate]]->fragment->Length < endWake)
					{
						endWake = Math::Max(0, candidates[iCandidate] - f->max[fragmentIndex[iCandidate]]->fragment->Length); // no +1 as we want to include the NEXT symbol
					}
					Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " Max Fragment " + f->max[fragmentIndex[iCandidate]]->fragment + " @ " + candidates[iCandidate] + ".." + (endWake+1));

					for (size_t iLength = 0; iLength < f->max[fragmentIndex[iCandidate]]->fragment->Length; iLength++)
					{
						if (candidates[iCandidate] - iLength <= startLocalizationLimit && candidates[iCandidate] - iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidates[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_Strong);
						}
					}
				}
			}

			// Set the localization for the mid fragments
			if ((localizeMidFragment) && (candidatesMid->Count > 0))
			{
				for (size_t iCandidate = 0; iCandidate < candidatesMid->Count; iCandidate++)
				{
					Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " Mid Fragments " + f->mid->fragment + " @ " + candidatesMid[iCandidate]);
					for (size_t iLength = 0; iLength < f->mid->fragment->Length; iLength++)
					{
						if (candidatesMid->Count > 1 && candidatesMid[iCandidate] - iLength <= startLocalizationLimit && candidatesMid[iCandidate] - iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidatesMid[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_Strong);
						}
						else if (candidatesMid->Count == 1 && candidatesMid[iCandidate] - iLength <= startLocalizationLimit && candidatesMid[iCandidate] - iLength >= endLocalizationLimit)
						{
							this->MAO->SetLocalization(iGen, candidatesMid[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_Strong);
						}
					}
				}
			}

//			// Any max fragment that could not be placed in the wake is tabu
//			List<Fragment^>^ toRemove = gcnew List<Fragment^>;
//			for (size_t iFragment = 0; iFragment < f->max->Count; iFragment++)
//			{
//				// remove any max fragment that could not be placed in the wake as false
//				if (!fragmentIndex->Contains(iFragment))
//				{
//#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
//					Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " max fragment " + f->max[iFragment]->fragment + " is tabu");
//#endif
//					toRemove->Add(f->max[iFragment]);
//				}
//				Console::Write("");
//			}
//			this->MAO->RemoveFact_MaxFragmentOnly(f, toRemove, true);

			if ((startWakeAbs < startWake) || (startWake == 0))
			{
				startWake = startWakeAbs;
			}

			if (startLocalizationLimit < startWake)
			{
				startWake = startLocalizationLimit;
			}

			if ((endWakeAbs > endWake) || (endWake == 99999))
			{
				endWake = endWakeAbs;
			}

			if (endLocalizationLimit > endWake)
			{
				endWake = endLocalizationLimit;
			}

			prevStart = startWake;
			prevEnd = endWake;
		}
	}
}
        """
        pass

    def right_left_localization_btf_only(self):
        """
void LSIProblemV3::ComputeSymbolLocalization_RightToLeftLocalization_BTFOnly(Int32 iGen)
{
	Console::WriteLine("Right to Left Localization BTF Only");
	Console::WriteLine("===================================");
	Int32 prevStart = this->model->evidence[iGen + 1]->Length() - 1;
	Int32 prevEnd = this->model->evidence[iGen + 1]->Length() - 1;
	bool prevIsTurtle = false;
	bool prevSingleCandidate = false;
	bool prevComplete = false;

	Console::WriteLine();
	//this->MAO->localization[iGen] = gcnew array<Byte, 2>(this->model->evidence[iGen + 1]->Length(), this->model->evidence[iGen]->Length());

	for (Int16 iPos = this->model->evidence[iGen]->Length() - 1; iPos >= 0; --iPos)
	{
#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
		Console::WriteLine(iPos + ": " + this->model->evidence[iGen]->GetSymbol(iPos) + " in wake from " + prevStart + " to " + prevEnd);
#endif
		Int32 symbolIndex = this->model->evidence[iGen]->GetSymbolIndex(iPos);

		List<Int32>^ candidates = gcnew List<Int32>;

		if (this->model->alphabet->IsTurtle(symbolIndex))
		{
			prevIsTurtle = true;
			// All turtle symbols must be in the prev range or the right neighbour of the range
			// Look to find all the places where the symbol matches
			for (Int16 iScan = prevStart; iScan >= prevEnd; --iScan)
			{
				if (iScan < this->model->evidence[iGen + 1]->Length()) // if the previous symbols range already extends to the end then don't scan outside the word
				{
					if ((symbolIndex == this->model->evidence[iGen + 1]->GetSymbolIndex(iScan)) && (this->ValidateLeftNeighbourTurtle(this->model->evidence[iGen], this->model->evidence[iGen + 1], iPos - 1, iScan - 1)))
					{
						candidates->Add(iScan);
					}
				}
			}

			if (candidates->Count == 1)
			{
				prevSingleCandidate = true;
				this->MAO->SetLocalization(iGen, candidates[0], iPos, MasterAnalysisObject::cLocalization_Locked);
			}
			else
			{
				prevSingleCandidate = false;
				for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
				{
					// Upgrade the setting from weak to strong
					this->MAO->SetLocalization(iGen, candidates[iCandidate], iPos, MasterAnalysisObject::cLocalization_Strong);
				}
			}

			prevStart = candidates[0] - 1;
			prevEnd = candidates[candidates->Count - 1] - 1;
		}
		else
		{
			// if the prev symbol is a turtle, AND only had a single candidate
			// then this create a head fragment for the current symbol
			if ((prevIsTurtle) && (prevSingleCandidate))
			{
				prevSingleCandidate = true;
				this->ComputeFragment_Position_TailOnly(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevStart);
			}

			// Set the localization for the head fragments
			Fact^ f = this->MAO->GetFact(iGen, this->model->evidence[iGen], iPos);
			// Adjust the wake based on the WTW
			Range^ wtw = this->model->evidence[iGen]->GetWTW(iPos);
			if (prevStart < wtw->start)
			{
				prevStart = wtw->start;
			}
			if (prevEnd > wtw->end)
			{
				prevEnd = wtw->start;
			}

			List<Int32>^ candidatesBTF = gcnew List<Int32>;
			Int32 startWake = 0;
			Int32 endWake = 99999;
			Int32 startLocalizationLimit = 0;
			Int32 endLocalizationLimit = 99999;
			prevIsTurtle = false;
			FragmentSigned^ btf;

			if (f->btf->Count == 1)
			{
				btf = f->btf[0];
				this->model->evidence[iGen]->SetBTF(iPos, f->btf[0]);
			}
			else
			{
				btf = this->model->evidence[iGen]->GetBTF(iPos);
			}

			for (Int16 iScan = prevStart; iScan >= prevEnd; --iScan)
			{
				if (iScan < this->model->evidence[iGen + 1]->Length())
				{
					Int32 start = iScan - btf->fragment->Length + 1;
					Int32 end = start + btf->fragment->Length;
					if (start >= 0)
					{
						String^ subword = this->model->evidence[iGen + 1]->GetSymbols(start, btf->fragment->Length);
						if (subword == btf->fragment && (iScan <= wtw->end && iScan >= wtw->start))
						{
							candidatesBTF->Add(iScan);
						}
					}
				}
			}

			// If no BTF could be placed in the wake, then create a new BTF and localize it
			// A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
			// -- if this fails then it means the BTF comes from an instance with a non-compatible signature
			// B. Create a BTF by considering the max fragments. A BTF is formed from the start of the wake to the end of the next wake.
			// C. Create a BTF using the reserve algorithm
			if (candidatesBTF->Count == 0)
			{
				Fragment^ toCache;
				Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + btf->fragment + " cannot be localized in wake " + this->model->evidence[iGen + 1]->GetSymbolsFromPos(prevEnd, prevStart));

				// A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
				// -- if this fails then it means the BTF comes from an instance with a non-compatible signature
				toCache = this->ComputeBTF_LocalizationCompatability_RightToLeft(btf, this->model->evidence[iGen + 1], prevEnd, prevStart);

				//// A. Try to check the existing BTF for localization compatability. Extend the wake and see if it localizes.
				//// -- if this fails then it means the BTF comes from an instance with a non-compatible signature
				//Int32 iBTF = 0;
				//bool btfFound = false;
				//do
				//{
				//	btf = this->ComputeBTF_LocalizationCompatability_RightToLeft(f->btf[iBTF], this->model->evidence[iGen + 1], prevEnd, prevStart);
				//	if (btf->fragment != nullptr)
				//	{
				//		btfFound = true;
				//		Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by localization compatibility BTF " + btf->fragment);
				//	}
				//	else
				//	{
				//		Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + f->btf[iBTF]->fragment + " is not locally compatible.");
				//	}
				//	iBTF++;
				//} while (!btfFound && iBTF < f->btf->Count);

				//// B. Create a BTF by considering the max fragments. A BTF is formed from the start of the wake to the end of the next wake.
				//if (btf->fragment == nullptr && candidates->Count > 0)
				//{
				//	Int32 btfStart = 99999;
				//	Int32 btfEnd = prevStart;
				//	for (size_t iCandidate = 0; iCandidate < candidates->Count; iCandidate++)
				//	{
				//		if (btfStart > candidates[iCandidate] - f->max[fragmentIndex[iCandidate]]->fragment->Length)
				//		{
				//			btfStart = Math::Max(0, candidates[iCandidate] - f->max[fragmentIndex[iCandidate]]->fragment->Length);
				//		}
				//	}
				//	btf = this->MAO->CreateFragment(this->model->evidence[iGen + 1]->GetSymbolsFromPos(btfStart, btfEnd),false,true);
				//	Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found from max fragments BTF " + btf->fragment);
				//}

				// C. Create a BTF using the reserve algorithm
				//if (toCache->fragment == nullptr)
				//{
				//	toCache = this->ComputeFragment_Position_BTFOnly_RightToLeft(iGen, this->model->evidence[iGen], iPos, this->model->evidence[iGen + 1], prevEnd,prevStart);
				//	Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by position reserve BTF " + toCache->fragment);
				//}

				f->cache->Add(this->MAO->CreateBTF(toCache, btf->leftSignature, btf->rightSignature));
				this->MAO->SetFact_BTFOnly_Update(btf, f->cache[f->cache->Count - 1], f);
				Console::WriteLine("For SAC " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " found by localization compatibility BTF " + btf->fragment);
				candidatesBTF = this->ComputeSymbolLocalization_MaxFragment_RightToLeft(btf, this->model->evidence[iGen + 1], prevEnd, prevStart);
			}

			for (size_t iCandidate = 0; iCandidate < candidatesBTF->Count; iCandidate++)
			{
				Console::WriteLine("Localizing " + this->MAO->SymbolCondition(iGen, this->model->evidence[iGen], iPos) + " BTF " + btf->fragment + " @ " + candidatesBTF[iCandidate] + ".." + (1 + candidatesBTF[iCandidate] - btf->fragment->Length));

				if (candidatesBTF[iCandidate] - f->length->min > startWake)
				{
					startWake = candidatesBTF[iCandidate] - f->length->min;
				}
				if (candidatesBTF[iCandidate] > startLocalizationLimit)
				{
					startLocalizationLimit = candidatesBTF[iCandidate];
				}

				if (candidatesBTF[iCandidate] - btf->fragment->Length < endWake)
				{
					endWake = candidatesBTF[iCandidate] - btf->fragment->Length;
				}
				if (candidatesBTF[iCandidate] - btf->fragment->Length + 1 < endLocalizationLimit)
				{
					endLocalizationLimit = candidatesBTF[iCandidate] - btf->fragment->Length + 1;
				}

				for (size_t iLength = 0; iLength < btf->fragment->Length; iLength++)
				{
					this->MAO->SetLocalization(iGen, candidatesBTF[iCandidate] - iLength, iPos, MasterAnalysisObject::cLocalization_StrongBTF);
				}
			}

			startLocalizationLimit = Math::Min(prevStart, startLocalizationLimit);
			endLocalizationLimit = Math::Max(0, Math::Max(prevEnd - f->length->max + 1, endLocalizationLimit));

			Console::WriteLine("Absolute localization limit is " + startLocalizationLimit + " / " + endLocalizationLimit);

			if (startLocalizationLimit < startWake)
			{
				startWake = startLocalizationLimit;
			}

			if (endLocalizationLimit - 1 > endWake)
			{
				endWake = endLocalizationLimit - 1;
			}

			prevStart = startWake;
			prevEnd = endWake;

			if (iGen >= 999)
			{
				Console::ReadLine();
			}
		}
	}
}
        """
        pass

    def left_right_localization_max_fragment(self):
        """
List<Int32>^ LSIProblemV3::ComputeSymbolLocalization_MaxFragment_LeftToRight(Fragment^ Fr, WordXV3^ W, Int32 StartWake, Int32 EndWake)
{
	List<Int32>^ result = gcnew List<Int32>;
	for (size_t iScan = StartWake; iScan <= EndWake; iScan++)
	{
		if (iScan < W->Length())
		{
			// find a candidate for the BTF
			String^ subwordMax = W->GetSymbols(iScan, Fr->fragment->Length);
			if (subwordMax == Fr->fragment)
			{
				result->Add(iScan);
			}
		}
	}

	return result;
}
        """
        pass

    def right_left_localization_max_fragment(self):
        """
List<Int32>^ LSIProblemV3::ComputeSymbolLocalization_MaxFragment_RightToLeft(Fragment^ Fr, WordXV3^ W, Int32 StartWake, Int32 EndWake)
{
	List<Int32>^ result = gcnew List<Int32>;
	for (size_t iScan = StartWake; iScan <= EndWake; iScan++)
	{
		if (iScan < W->Length())
		{
			Int32 start = iScan - Fr->fragment->Length + 1;
			if (start >= 0)
			{
				String^ subwordMax = W->GetSymbols(start, Fr->fragment->Length);
				if (subwordMax == Fr->fragment)
				{
					result->Add(iScan);
				}
			}
		}
	}

	return result;
}
        """
        pass

    def localization(self):
        """
void LSIProblemV3::ComputeSymbolLocalization()
{
#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
	Console::WriteLine();
	Console::WriteLine("Computing Symbol Localization");
	Console::WriteLine("=============================");
#endif
	// A. Perform BTF Only localization until convergence
	do
	{
		this->MAO->ResetBTFChangeFlag();
		for (size_t iGen = 0; iGen < this->model->generations - 1; iGen++)
		{
			// Step 1. Perform left to right localization
			this->ComputeSymbolLocalization_LeftToRightLocalization_BTFOnly(iGen);
#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
			Console::WriteLine("Before Right to Left");
			Console::WriteLine("********************");
			for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
			{
				Console::Write(iPos2 + " : " + this->model->evidence[iGen + 1]->GetSymbol(iPos2) + " : ");
				for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
				{
					if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_WeakBTF)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + ")");
					}
					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "!)");
					}
				}
				Console::WriteLine();
			}
			Console::WriteLine();
#endif
			// Step 2. Perform right to left localization
			this->ComputeSymbolLocalization_RightToLeftLocalization_BTFOnly(iGen);

#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
			Console::WriteLine("Before Weak Removal");
			Console::WriteLine("*******************");
			for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
			{
				Console::Write(iPos2 + " : " + this->model->evidence[iGen + 1]->GetSymbol(iPos2) + " : ");
				for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
				{
					if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_WeakBTF)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + ")");
					}
					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "*)");
					}
					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "!)");
					}
				}
				Console::WriteLine();
			}
			Console::WriteLine();
#endif

			// Step 3. Remove all weak localizations
			for (Int32 iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
			{
				for (Int32 iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
				{
					if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_WeakBTF) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Unset))
					{
						this->MAO->SetLocalization(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Never);
					}
				}
			}

#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
			Console::WriteLine("Before Analysis");
			Console::WriteLine("***************");
			for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
			{
				Console::Write(iPos2 + " : " + this->model->evidence[iGen + 1]->GetSymbol(iPos2) + " : ");
				for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
				{
					if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_WeakBTF)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + ")");
					}
					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "*)");
					}
					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "!)");
					}
				}
				Console::WriteLine();
			}
			Console::WriteLine();
#endif
			// Step 4. Analyze
			this->ComputeSymbolLocalization_Analyze_BTFOnly(iGen);

#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
			Console::WriteLine("After Analysis");
			Console::WriteLine("**************");
			for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
			{
				Console::Write(iPos2 + " : " + this->model->evidence[iGen + 1]->GetSymbol(iPos2) + " : ");
				for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
				{
					if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_WeakBTF)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + ")");
					}
					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "*)");
					}
					else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
					{
						Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "!)");
					}
				}
				Console::WriteLine();
			}
			Console::WriteLine();
#endif

			// Step 5. Build a new set of BTFs
			this->ComputeBTF_Localization(iGen);
			// ??? Should this only be running after all the generations are completed?
			this->ComputeBTF_Cache();
#if _PHASE3_COMPUTE_FRAGMENTS_CACHE_ >= 1
			this->MAO->Display();
#endif
		}

		// Reset all the localizations to unset
		if (this->MAO->HasBTFChangeOccured())
		{
			for (size_t iGen = 0; iGen < this->model->generations-1; iGen++)
			{
				for (Int32 iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
				{
					for (Int32 iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
					{
						if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF && this->MAO->localization[iGen][iPos2, iPos1] != MasterAnalysisObject::cLocalization_Locked)
						{
							this->MAO->SetLocalization_Direct(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Unset);
						}
						else if (this->MAO->localization[iGen][iPos2, iPos1] != MasterAnalysisObject::cLocalization_Locked)
						{
							this->MAO->SetLocalization_Direct(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Never);
						}
					}
				}
			}
		}
	} while (this->MAO->HasBTFChangeOccured());

	// TODO: tomorrow morning... need to create the max fragments here

	// B. Perform head/tail/max/mid fragment localization
	for (size_t iGen = 0; iGen < this->model->generations - 1; iGen++)
	{
		this->ComputeSymbolLocalization_LeftToRightLocalization(iGen);

		// Remove all BTF localizations
		for (Int32 iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
		{
			for (Int32 iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
			{
				if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_WeakBTF) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_StrongBTF) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Unset))
				{
					this->MAO->SetLocalization(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Never);
				}
			}
		}

#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
		Console::WriteLine("Before Right to Left");
		Console::WriteLine("********************");
		for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
		{
			Console::Write(iPos2 + " : " + this->model->evidence[iGen + 1]->GetSymbol(iPos2) + " : ");
			for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
			{
				if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Weak)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + ")");
				}
				else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "*)");
				}
				else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "!)");
				}
			}
			Console::WriteLine();
		}
		Console::WriteLine();
#endif

		this->ComputeSymbolLocalization_RightToLeftLocalization(iGen);

#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
		Console::WriteLine("Before Weak Removal");
		Console::WriteLine("*******************");
		for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
		{
			Console::Write(iPos2 + " : " + this->model->evidence[iGen + 1]->GetSymbol(iPos2) + " : ");
			for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
			{
				if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Weak)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + ")");
				}
				else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "*)");
				}
				else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "!)");
				}
			}
			Console::WriteLine();
		}
		Console::WriteLine();
#endif

		// Remove all weak localizations
		for (Int32 iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
		{
			for (Int32 iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
			{
				if ((this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Weak) || (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Unset))
				{
					this->MAO->SetLocalization(iGen, iPos2, iPos1, MasterAnalysisObject::cLocalization_Never);
				}
			}
		}

#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
		Console::WriteLine("Before Analysis");
		Console::WriteLine("***************");
		for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
		{
			Console::Write(iPos2 + " : " + this->model->evidence[iGen + 1]->GetSymbol(iPos2) + " : ");
			for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
			{
				if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Weak)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + ")");
				}
				else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "*)");
				}
				else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "!)");
				}
			}
			Console::WriteLine();
		}
		Console::WriteLine();
#endif

		this->ComputeSymbolLocalization_Analyze(iGen);

#if _PHASE3_COMPUTE_LOCALIZATION_ >= 1
		Console::WriteLine("After Analysis");
		Console::WriteLine("***************");
		for (size_t iPos2 = 0; iPos2 < this->model->evidence[iGen + 1]->Length(); iPos2++)
		{
			Console::Write(iPos2 + " : " + this->model->evidence[iGen + 1]->GetSymbol(iPos2) + " : ");
			for (size_t iPos1 = 0; iPos1 < this->model->evidence[iGen]->Length(); iPos1++)
			{
				if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Weak)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + ")");
				}
				else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Strong)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "*)");
				}
				else if (this->MAO->localization[iGen][iPos2, iPos1] == MasterAnalysisObject::cLocalization_Locked)
				{
					Console::Write(this->model->evidence[iGen]->GetSymbol(iPos1) + "(" + iPos1 + "!)");
				}
			}
			Console::WriteLine();
		}
		Console::WriteLine();
#endif

		this->ComputeFragments_Localization(iGen);
	}
}
        """
        pass

    def compare_position(self):
        pass

    def compute_symbol_counts(self):
        """
        Compute the growth of words by analyzing the frequency of symbols
        in subsequent words within the evidence data.

        This function iterates through each word in the `problem.evidence.words` list (excluding the last word).
        For each symbol in the alphabet, it counts the occurrences of the symbol in the next word's
        `original_string`. The count is then stored in the `word_growth` attribute, indexed by the
        current word's index and the symbol's unique ID in the alphabet.
        """
        for iWord, w in enumerate(self.problem.evidence.words):
            for symbol in self.problem.evidence.alphabet.symbols:
                count = self.problem.evidence.words[iWord].original_string.count(symbol)
                self.symbol_counts[iWord][self.problem.evidence.alphabet.get_id(symbol)] = count

    def compute_unaccounted_growth_matrix(self):
        """
        Compute the unaccounted growth of symbols for each word in the evidence data.

        This function calculates the difference between the total growth of a symbol in a word
        and the growth of the symbol that can be attributed to specific structures (SACs).

        For each symbol in the alphabet and each word (excluding the last word):
            - Calculate the accounted growth of the symbol in the word based on SAC counts.
            - Subtract the accounted growth from the total growth to determine the unaccounted growth.
        """
        for symbol in self.problem.evidence.alphabet.symbols:
            for iWord, w in enumerate(self.problem.evidence.words[:-1]):
                accounted_growth_of_symbol_in_word = 0
                for iSaC, sac in enumerate(self.problem.evidence.sacs):
                    if sac in w.sac_counts:
                        min_growth_of_symbol_by_sac = self.min_growth[iSaC][
                            self.problem.evidence.alphabet.get_id(symbol)]
                        sac_count = w.sac_counts[sac]
                        accounted_growth_of_symbol_in_word += min_growth_of_symbol_by_sac * sac_count
                self.word_unaccounted_growth[iWord][self.problem.evidence.alphabet.get_id(symbol)] = (self.symbol_counts[iWord+1][self.problem.evidence.alphabet.get_id(symbol)] - accounted_growth_of_symbol_in_word)

    def compute_unaccounted_length_matrix(self):
        """
        Compute the unaccounted length for each word in the evidence data.

        This function calculates the difference between the total length of the next word
        and the length that can be attributed to specific structures (SACs).

        For each word (excluding the last word):
            - Calculate the accounted length based on SAC counts and their minimum lengths.
            - Subtract the accounted length from the total length of the next word to determine
              the unaccounted length.
        """
        for iWord, w in enumerate(self.problem.evidence.words[:-1]):
            accounted_length_in_word = 0
            for iSaC, sac in enumerate(self.problem.evidence.sacs):
                if sac in w.sac_counts:
                    min_length_by_sac = self.min_length[iSaC]
                    sac_count = w.sac_counts[sac]
                    accounted_length_in_word += min_length_by_sac * sac_count
            self.word_unaccounted_length[iWord] = len(self.problem.evidence.words[iWord+1]) - accounted_length_in_word

    def compute_total_length_symbiology(self):
        """
        DEPRECATED
        The general case of compute_length_total_length() covers this special case
        """
        print("compute_total_length_symbiology() is deprecated. Do not call.")
        pass
        #The total length of generation N can be reduced by the lengths of the SACs from previous generations
        #Thus the effect is a length equation for only those SACs that appear in this generation
        #for iWord, w in enumerate(self.problem.evidence.words[:-1]):
            #min_length = 0
            #max_length = 0
            #new_sac_counts = {}
            #next_word = self.problem.evidence.words[iWord+1]
            # find all new sacs in the next word
            #    if sac in prev.sac_counts:
            #        min_length += self.get_min_length(sac) * prev.sac_counts[sac]
            #        max_length += self.get_max_length(sac) * prev.sac_counts[sac]
            #       pass
            #    else:
            #        new_sac_counts[sac](w.sac_counts[iSac])
            #if len(new_sac_counts) > 0:
            #    #otherwise create an equation
            #    unaccounted_max = len(w) - min_length
            #    unaccounted_min = len(w) - max_length
            #    self.length_equations.append(create_length_equation(new_sac_counts, unaccounted_min, unaccounted_max))

    def naive_min_max(self):
        """
        This function processes the evidence from the `problem` object, updating matrices that track the
        minimum and maximum growth and length associated with each `sac` (Symbolic Alphabet Component). The
        computation depends on whether each `sac` belongs to the set of `identities` or not.

        Key steps include:
        - Setting `min_growth` and `max_growth` for each `sac` based on its presence in `identities`.
        - Determining `min_length` and `max_length` based on the shortest word length following the appearance
          of a `sac` in the provided list of evidence words.
        """
        sacs = self.problem.evidence.sacs
        identities = self.problem.evidence.alphabet.identities_ids
        naive_min = self.problem.absolute_min_length

        # Compute min and max growth
        for iSac, sac in enumerate(sacs):
            if sac.symbol in identities:
                self.min_growth[iSac][sac.symbol] = 1
                self.max_growth[iSac][sac.symbol] = 1
            else:
                self.min_growth[iSac][sac.symbol] = 0
                self.max_growth[iSac][sac.symbol] = 0

        shortest_word_length = max(len(word) for word in self.problem.evidence.words[1:])

        for iSac, sac in enumerate(sacs):
            if sac.symbol in identities:
                self.min_length[iSac] = 1
                self.max_length[iSac] = 1
            else:
                # find the shortest word after the sac appears
                for iWord, w in enumerate(self.problem.evidence.words[:-1]):
                    if sac in w.sacs:
                        shortest_word_length = len(self.problem.evidence.words[iWord+1])
                self.min_length[iSac] = naive_min
                self.max_length[iSac] = shortest_word_length

    # Core function to find the minimum set of sacs to solve all words
    def find_minimum_sacs_set(self):
        """
        Finds the minimum set of sacs required to solve all equations.

        Returns:
            set: The minimum set of sacs needed to solve all words.
        """
        uncovered_words = set(word for word in self.problem.evidence.words)
        selected_sacs = set()
        found_sacs = set()

        # Add all identity sacs to selected_sacs
        for sac in self.problem.evidence.sacs:
            if self.is_sac_identity(sac):
                selected_sacs.add(sac)

        # Loop until all words are covered
        while uncovered_words:
            # Count how many uncovered words each sac can solve
            sac_coverage = {}
            for word in uncovered_words:
                word_obj = next((w for w in self.problem.evidence.words if w == word), None)
                if word_obj:
                    for sac in word_obj.sac_counts.keys():
                        # Only consider sacs that have not already been selected
                        if sac not in selected_sacs and sac not in found_sacs:
                            sac_coverage[sac] = sac_coverage.get(sac, 0) + 1

            # Select the sac that solves the most uncovered words
            if not sac_coverage:
                raise RuntimeError("No valid sac can cover remaining words.")

            best_sac = max(sac_coverage, key=sac_coverage.get)
            selected_sacs.add(best_sac)

            # Remove all words that are now fully covered (explicitly or implicitly)
            while True:
                new_found_sacs = set()
                uncovered_words = {
                    word for word in uncovered_words
                    if not all(
                        sac in selected_sacs or sac in found_sacs or
                        all(
                            other_sac in selected_sacs or other_sac in found_sacs
                            for other_sac in next(
                                (w.sac_counts.keys() for w in self.problem.evidence.words if w == word), []
                            )
                            if other_sac != sac
                        )
                        for sac in next(
                            (w.sac_counts.keys() for w in self.problem.evidence.words if w == word), []
                        )
                    ) or new_found_sacs.update(
                        sac for sac in next(
                            (w.sac_counts.keys() for w in self.problem.evidence.words if w == word), []
                        ) if sac not in selected_sacs and sac not in found_sacs
                    )
                }
                if new_found_sacs:
                    found_sacs.update(new_found_sacs)
                else:
                    break

        # remove identities
        for sac in self.problem.evidence.sacs:
            if self.is_sac_identity(sac):
                selected_sacs.remove(sac)

        return selected_sacs

    # Core function to find the smallest p-space of sacs
    def find_smallest_pspace(self):
        """
        Finds the smallest p-space of sacs to solve all equations.

        Args:
            problem (Problem): The problem containing words and sacs.
            min_length (dict): A dictionary mapping each sac to its minimum length.
            max_length (dict): A dictionary mapping each sac to its maximum length.

        Returns:
            tuple: A set of sacs that minimizes the p-space and the p-space product.
        """
        uncovered_words = set(word for word in self.problem.evidence.words)
        selected_sacs = set()
        found_sacs = set()

        # Add all identity sacs to selected_sacs
        for sac in self.problem.evidence.sacs:
            if self.is_sac_identity(sac):
                selected_sacs.add(sac)

        total_product = 1

        # Loop until all words are covered
        while uncovered_words:
            # Evaluate the impact of adding each sac to the solution
            best_sac = None
            best_increase = float('inf')

            for sac in self.problem.evidence.sacs:
                if sac in selected_sacs or sac in found_sacs:
                    continue  # Already selected or found

                # Compute range product increase
                range_size = self.get_max_length(sac) - self.get_min_length(sac) + 1
                new_product = total_product * range_size

                # Count how many uncovered words this sac can solve
                covers = sum(1 for word in uncovered_words if sac in next(
                    (w.sac_counts.keys() for w in self.problem.evidence.words if w == word), []
                ))

                # Heuristic: prioritize sacs that solve more words with minimal range impact
                if covers > 0 and new_product < best_increase:
                    best_sac = sac
                    best_increase = new_product

            # Add the best sac to the solution
            selected_sacs.add(best_sac)
            total_product = best_increase

            # Remove all words that are now fully covered (explicitly or implicitly)
            while True:
                new_found_sacs = set()
                uncovered_words = {
                    word for word in uncovered_words
                    if not all(
                        sac in selected_sacs or sac in found_sacs or
                        all(
                            other_sac in selected_sacs or other_sac in found_sacs
                            for other_sac in next(
                                (w.sac_counts.keys() for w in self.problem.evidence.words if w == word), []
                            )
                            if other_sac != sac
                        )
                        for sac in next(
                            (w.sac_counts.keys() for w in self.problem.evidence.words if w == word), []
                        )
                    ) or new_found_sacs.update(
                        sac for sac in next(
                            (w.sac_counts.keys() for w in self.problem.evidence.words if w == word), []
                        ) if sac not in selected_sacs and sac not in found_sacs
                    )
                }
                if new_found_sacs:
                    found_sacs.update(new_found_sacs)
                else:
                    break

        # Remove all identity sacs to selected_sacs
        for sac in self.problem.evidence.sacs:
            if self.is_sac_identity(sac):
                selected_sacs.remove(sac)

        return selected_sacs, total_product
