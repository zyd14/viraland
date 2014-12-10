#include <iostream>
#include <fstream>
#include <cstring>
#include <stdlib.h>

using namespace std;

class genome
{
    public:
    int num_proteins;       //number of proteins in this genome
    char ** proteins;       //1D array of the protein accession numbers (names)
    int * counts;           //number of times the protein is hit (indices of counts correspond with the indices of proteins)
    char * acc_genome;      //accession # of the genome
    char * spp_information; //organism's name

    genome();
    bool initialize(int i, char * accession, char * spp);
    bool initialize_counts();
    bool add_protein(int i, char * val);
    int get_number_of_hits_to_genome();
    int get_number_of_proteins_with_hits();
    bool get_number_of_hits_by_protein(char **& protein_id, int *& vals);
    bool show_number_of_hits_by_protein();
    float get_percentage_of_proteins_hit();
    bool increment_hits_counter(int index);
    bool show_hits();
    ~genome();
};

genome::genome()
{
    num_proteins=0;
}

bool genome::initialize(int i, char * accession, char * spp)
{
    num_proteins=i;
    acc_genome=new char [strlen(accession)+1];
    sprintf(acc_genome,"%s",accession);
    spp_information=new char [strlen(spp)+1];
    sprintf(spp_information,"%s",spp);

    proteins=new char * [num_proteins];
    counts=new int [num_proteins];
    initialize_counts();
}

bool genome::initialize_counts()
{
    int i;
    for(i=0;i<num_proteins;i++) counts[i]=0;
    return true;
}

bool genome::add_protein(int i, char * val)
{
    if(i<num_proteins)
    {
        proteins[i]=new char [strlen(val)+1];
        sprintf(proteins[i],"%s",val);
        return true;
    }
    else return false;
}

int genome::get_number_of_hits_to_genome()
{
    int i;
    int total=0;
    for(i=0;i<num_proteins;i++) total+=counts[i];
    return total;
}


int genome::get_number_of_proteins_with_hits()
{
    int i;
    int counter=0;
    for(i=0;i<num_proteins;i++)
    {
        if(counts[i]>0) counter++;
    }
    return counter;
}

bool genome::get_number_of_hits_by_protein(char **& protein_id, int *& vals)
{
    if(vals!=NULL) delete vals;
    vals=new int [num_proteins];
    if(protein_id!=NULL) delete protein_id;
    protein_id=new char * [num_proteins];
    int i;
    for(i=0;i<num_proteins;i++)
    {
        vals[i]=counts[i];
        protein_id[i]=new char [strlen(proteins[i])+1];
        sprintf(protein_id[i],"%",proteins[i]);
    }
    return true;
}

bool genome::show_hits()
{
    int i;
    for(i=0;i<num_proteins;i++)
    {
        if(counts[i]>0)
        {
            cout << proteins[i] << "\t" << counts[i] << endl;
        }
    }
}

bool genome::show_number_of_hits_by_protein()
{
    int i;
    for(i=0;i<num_proteins;i++)
    {
        cout << proteins[i] << "\t" << counts[i] << endl;
    }
    return true;
}


float genome::get_percentage_of_proteins_hit()
{
    int i;
    int n=0;
    for(i=0;i<num_proteins;i++)
    {
        if(counts[i]>0) n++;
    }
    return ((float)n/(float)num_proteins)*100.00;
}

bool genome::increment_hits_counter(int index)
{
    if(index<num_proteins) {counts[index]++; return true;}
    else return false;
}

genome::~genome()
{
    int i;
    for(i=0;i<num_proteins;i++) delete proteins[i];
    delete proteins;
    delete counts;
}

class super_file
{
    public:
    int num_genomes;        //number of genomes in faa collection
    genome * g;             //array of type genome

    super_file(int n, char * file);
    bool read_BLAST(char * file);
    bool read_BLAST(char * file, float evalue_threshold);
    bool is_in(char * acc, int & genome_num, int & gene_num);
    bool write_out_summary_statistics(char * output_file);
    bool write_out_forHitViz(char * output_file);
    bool write_out_forKrona(char * output_file);
    bool reset_counts();
    ~super_file();

    private:
    bool populate_genome(char * file);
    bool parse_hit_special_case(char *& hit, char *& prot_acc_num, char *& prot_function, char *& spp);
    bool parse_hit(char *& hit, char *& prot_acc_num, char *& prot_function, char *& spp);
};

super_file::super_file(int n, char * file)
{
    num_genomes=n;
    g=new genome [num_genomes];
    populate_genome(file);
    cout << "super_file set up\n";
}

bool super_file::populate_genome(char * file)
{
    int i;
    char * text=new char [100];
    char * spp=new char [100];
    char * prior_g=new char [100];
    int num_genes=0;
    int genome_index=0;

    ifstream in;

    //set up data structure
    in.open(file);
    if(!in.is_open())
    {
        cout << "Cannot open genome file.\n";
        delete text;
        delete prior_g;
        delete spp;
        in.clear();
        in.close();
        return false;
    }
    in.getline(prior_g,100,'\t'); num_genes++;
    in.getline(text,100,'\t');
    in.getline(spp,100,'\n');
    while(in.peek()!=EOF)
    {
        in.getline(text,100,'\t');
        if(strcmp(text,prior_g)==0)
            num_genes++;
        else
        {
            g[genome_index].initialize(num_genes,prior_g,spp);
            num_genes=1;
            genome_index++;
            sprintf(prior_g,"%s",text);
        }
        in.getline(text,100,'\t');
        in.getline(spp,100,'\n');
    }
    g[genome_index].initialize(num_genes,prior_g,spp);
    in.clear();
    in.close();

    in.open(file);
    genome_index=0;
    while(in.peek()!=EOF)
    {
        cout << g[genome_index].acc_genome << "\t" << g[genome_index].spp_information << endl;
        for(i=0;i<g[genome_index].num_proteins;i++)
        {
            in.getline(text,100,'\t');  //strip off the accession number
            in.getline(text,100,'\t');  //get protein id number
            g[genome_index].add_protein(i,text);
            in.getline(text,100,'\n');
        }
        genome_index++;
    }
    in.clear();
    in.close();

    delete text;
    delete prior_g;

    return true;
}

bool super_file::read_BLAST(char * file)
{
    ifstream in;
    in.open(file);
    if(!in.is_open()) {cout << "Cannot find file.\n"; return false;}

    char node[1000];
    char *hit=new char [1000];
    char junk[50];
    float evalue;
    int genome_num, gene_num;

    char * prot_acc_num;
    char * prot_function;
    char * spp;

    while(in.peek()!=EOF)
    {
        in.getline(node,1000,'\t');
        in.getline(hit,1000,'\t');
        in>>evalue;
        in.getline(junk,50,'\n');
        prot_acc_num=NULL; prot_function=NULL; spp=NULL;
        if(parse_hit(hit,prot_acc_num,prot_function,spp))
        {
            //update count
            if(is_in(prot_acc_num, genome_num, gene_num))
                g[genome_num].increment_hits_counter(gene_num);

        }
        delete prot_acc_num; delete prot_function; delete spp;

    }
    in.clear();
    in.close();

    delete hit;
    delete prot_acc_num;
    delete prot_function;
    delete spp;

    return true;
}

bool super_file::read_BLAST(char * file, float evalue_threshold)
{
    ifstream in;
    in.open(file);
    if(!in.is_open()) {cout << "Cannot find file.\n"; return false;}

    char node[1000];
    char *hit=new char [1000];
    char junk[50];
    float evalue;
    int genome_num, gene_num;

    char * prot_acc_num;
    char * prot_function;
    char * spp;

    while(in.peek()!=EOF)
    {
        in.getline(node,1000,'\t');
        in.getline(hit,1000,'\t');
        in>>evalue;
        in.getline(junk,50,'\n');
        if(evalue<=evalue_threshold)
        {
            prot_acc_num=NULL; prot_function=NULL; spp=NULL;
            if(parse_hit(hit,prot_acc_num,prot_function,spp))
            {
                //update count
                if(is_in(prot_acc_num, genome_num, gene_num))
                    g[genome_num].increment_hits_counter(gene_num);

            }
            delete prot_acc_num; delete prot_function; delete spp;
        }
    }
    in.clear();
    in.close();

    delete hit;
    delete prot_acc_num;
    delete prot_function;
    delete spp;

    return true;
}


bool super_file::is_in(char * acc, int & genome_num, int & gene_num)
{
    int i,j;
    for(i=0;i<num_genomes;i++)
    {
        for(j=0;j<g[i].num_proteins;j++)
        {
            if(strcmp(g[i].proteins[j],acc)==0)
            {
                genome_num=i; gene_num=j;
                return true;
            }
        }
    }
    genome_num=gene_num=0;
    return false;
}

bool super_file::write_out_forHitViz(char * output_file)
{
    int i,j,n;
    ofstream out;
    char file_name[300];

    //output #hits by protein
    sprintf(file_name,"HV_%s",output_file);
    out.open(file_name);
    for(i=0;i<num_genomes;i++)
    {
        n=g[i].get_number_of_hits_to_genome();
        if(n>0)
        {
            out << g[i].acc_genome << "|" << g[i].spp_information << "|" << endl;
            for(j=0;j<g[i].num_proteins;j++)
            {
                out << g[i].proteins[j] << "|" << g[i].counts[j] << "|" << endl;
            }
            out << "*" << endl;
        }
    }
    out.clear();
    out.close();

    return true;
}

bool super_file::write_out_forKrona(char * output_file)
{
    int i;
    ofstream out;

    //output coverage by genome
    out.open(output_file);
    out << "Accession Number\tSpp\tNumber of Proteins in Genome\tNumber of Hits to Genome\t% of Proteins Hit\n";
    for(i=0;i<num_genomes;i++)
    {
        out << g[i].acc_genome << "\t" << g[i].spp_information << "\t" << g[i].num_proteins << "\t";
        out << g[i].get_number_of_hits_to_genome() << "\t" << g[i].get_percentage_of_proteins_hit() << endl;
    }
    out.clear();
    out.close();

    return true;
}

bool super_file::write_out_summary_statistics(char * output_file)
{
    int i,j,n;
    ofstream out;
    char file_name[300];

    //output coverage by genome
    sprintf(file_name,"coverage_stats_%s",output_file);
    out.open(file_name);
    out << "Accession Number\tSpp\tNumber of Proteins in Genome\tNumber of Hits to Genome\t% of Proteins Hit\n";
    for(i=0;i<num_genomes;i++)
    {
        out << g[i].acc_genome << "\t" << g[i].spp_information << "\t" << g[i].num_proteins << "\t";
        out << g[i].get_number_of_hits_to_genome() << "\t" << g[i].get_percentage_of_proteins_hit() << endl;
    }
    out.clear();
    out.close();

    //output #hits by protein
    sprintf(file_name,"hits_by_protein_%s",output_file);
    out.open(file_name);
    for(i=0;i<num_genomes;i++)
    {
        n=g[i].get_number_of_hits_to_genome();
        if(n>0)
        {
            out << g[i].acc_genome << "\t" << g[i].spp_information << "\t" << n << endl;
            out << "Protein Acc #\tNumber of Hits to Protein\n";
            for(j=0;j<g[i].num_proteins;j++)
            {
                if(g[i].counts[j]>0) out << g[i].proteins[j] << "\t" << g[i].counts[j] << endl;
            }
            out << endl;
        }
    }
    out.clear();
    out.close();

    return true;
}

bool super_file::reset_counts()
{
   int i;
   for(i=0;i<num_genomes;i++)
        g[i].initialize_counts();
   return true;
}

super_file::~super_file()
{
    delete g;
}


/****  PARSING RESULTS FROM PAUDA  ****/

bool super_file::parse_hit_special_case(char *& hit, char *& prot_acc_num, char *& prot_function, char *& spp)
{
    int i, start_p, end_p;
    char * pch;

    if(hit[0]=='l')
    {
        //get protein accession number
        pch=strstr(hit,"protein_id=");
        start_p=pch-hit+11;
        pch=strchr(pch,']');
        end_p=pch-hit;
        prot_acc_num=new char [end_p-start_p+2];
        for(i=start_p;i<end_p;i++) prot_acc_num[i-start_p]=hit[i];
        prot_acc_num[i-start_p]='\0';

        //get protein function
        pch=strstr(hit,"protein=");
        start_p=pch-hit+8;
        pch=strchr(pch,']');
        end_p=pch-hit;
        prot_function=new char [end_p-start_p+2];
        for(i=start_p;i<end_p;i++) prot_function[i-start_p]=hit[i];
        prot_function[i-start_p]='\0';
/*
        //get spp
        for(i=0; i<9; i++) junk[i]=hit[i+4];
        junk[i]='\0';
        if(strcmp(junk,"NC_013597")==0) spp="Aggregatibacter phage S1249";
        if(strcmp(junk,"NC_002180")==0) spp="Chlamydia phage phiCPAR39";
        if(strcmp(junk,"NC_008265")==0) spp="Clostridium phage phiSM101";
        if(strcmp(junk,"NC_017732")==0) spp="Enterococcus phage EF62phi";
        if(strcmp(junk,"NC_016568")==0) spp="Helicobacter phage phiHP33";
        if(strcmp(junk,"NC_018285")==0) spp="Streptococcus phage YMC-2011";
        if(strcmp(junk,"NC_018264")==0) spp="Thermoanaerobacterium phage THSA-485A";
            */
    }
 /*   else
    {
        //get protein accession number
        start_p=0;
        pch=strchr(hit,'|');
        end_p=pch-hit;
        prot_acc_num=new char [end_p+11];

        for(i=start_p;i<end_p;i++) junk[i-start_p]=hit[i];
        junk[i-start_p]='\0';
        sprintf(prot_acc_num,"NC_020490_%s",junk);

        prot_function="Predicted protein by GeneMark.hmm";
        spp="Staphylococcus phage StB12";
    }*/
    return true;
}


bool super_file::parse_hit(char *& hit, char *& prot_acc_num, char *& prot_function, char *& spp)
{
    int i,j,start_p,end_p;
    char * pch;
    bool special_case=false;

    pch=strstr(hit,"lcl|");
    if(pch!=NULL) special_case=true;
    else
    {
        pch=strstr(hit,"GeneMark.hmm");
        if(pch!=NULL) special_case=true;
    }
    if(special_case)
    {
        parse_hit_special_case(hit,prot_acc_num,prot_function,spp);
        return true;
    }
    else
    {
        pch=strchr(hit,'|');
        if(pch==NULL)
        {
            cout << "format of gene not correct\n";
            return false;
        }
        pch=strchr(pch+1,'|');  //get second pipe

        //get accession
        pch=strchr(pch+1,'|');  //get third pipe
        start_p=pch-hit;
        pch=strchr(pch+1,'|');  //get fourth pipe
        end_p=pch-hit;
        j=end_p-start_p;
        prot_acc_num=new char [j+1];
        for(i=0;i<j-1;i++) prot_acc_num[i]=hit[start_p+1+i];
        prot_acc_num[i]='\0';

        //get function
        pch=strchr(pch+1,'[');  //get bracket
        if(pch==NULL)
        {
            cout << "format of gene not correct\n";
            return false;
        }
        start_p=end_p+1;
        end_p=pch-hit;
        j=end_p-start_p+1;
        prot_function=new char [j+1];
        while(hit[start_p]==' ') {start_p++; j--;}
        for(i=0;i<j-1;i++) prot_function[i]=hit[start_p+i];
        if(prot_function[i-1]==' ') i--;
        prot_function[i]='\0';

        //get species
        pch=strchr(pch+1,']');  //get bracket
        start_p=end_p+1;
        end_p=pch-hit;
        j=end_p-start_p+1;
        spp=new char[j+1];
        for(i=0;i<j-1;i++) spp[i]=hit[start_p+i];
        spp[i]='\0';

        return true;
    }
}



/* It assumes you are given the number of genomes and the file that has the 
 * proteins listed for genomes user/caller needs to specify the name of the pauda
 * output file and the e-value threshold all output files are writen to the
 * directory containing the code... this can be changed by passing in the path
 * with the calls to the functions
 */

int main(int argc, char * argv []) {
	
	if (argc != 4) {	
		cout << "Usage: ./main [FAA List File] [PAUDA Output File] [# of Proteins in FAA]\n";
		exit(1);
	}
	
    int i;
    char *samples=new char [50];
    int num_proteins_in_faa_file= atoi(argv[3]);
    char * faa_list_file = argv[1];

    super_file s(num_proteins_in_faa_file,faa_list_file);

    char * pauda_output_file=argv[2];
    float threshold=0.001;
    s.read_BLAST(pauda_output_file,threshold);

    //for HitViz
    s.write_out_forHitViz(pauda_output_file);

    //for Krona
    s.write_out_forKrona(pauda_output_file);

    //for Statistics Files
    s.write_out_summary_statistics(pauda_output_file);

    s.~super_file();

    return 1;
}
