import scrapy
from scrapy.crawler import CrawlerProcess

class pdb_scraper(scrapy.Spider):
	name = 'pdb_scraper'

	def start_requests(self):
		f_IDs = open('data/pdbIDs_separated.txt', 'r')

		custom_settings = {
		'DOWNLOAD_DELAY': 1,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 2
		}

		for ID in f_IDs:
			url = 'https://www.rcsb.org/pdb/explore/sequenceText.do?structureId={}&chainId=A'.format(ID.strip('\n'))

			yield scrapy.Request(url=url, callback=self.parse_fetch)

	def parse_fetch(self, response):
		print('\n\n Entered Here \n\n')

		global aa_seq, aa_label

		aa_seq = response.xpath('''//td[@class="reportsequence" and @alt="entity_poly.pdbx_seq_one_letter_code"]/
								font[@class="reportsequence"]/text()''').extract()

		aa_label = response.xpath('''//tr[@class="reportsequence"]/td[@class="reportsequence" 
								and @align="left" and not(@alt="entity_poly.pdbx_seq_one_letter_code")]/text()''').extract()

		fin_aa_label = []

		for line_label in aa_label[1::2]:
			line_label = line_label.strip('\n').replace('\xa0', 'N')
			line_label = [label for label in line_label]
			del line_label[10::11]

			fin_aa_label.append(''.join(line_label))

		fin_aa_label = ''.join(fin_aa_label)
		fin_aa_seq = ''.join(aa_seq)

		f.write('%s %s\n' %(fin_aa_seq, fin_aa_label))

f = open('data/seqWithLabel2.txt', 'a+')

process = CrawlerProcess()
process.crawl(pdb_scraper)
process.start()

f.close()