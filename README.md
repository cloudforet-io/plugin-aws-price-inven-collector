# plugin-aws-price-info-

Plugin for AWS Price info
- Collecting AWS Product include pricing info

# Data Structure

## Product

~~~
"data": {
	"service_code": "AmazonEC22",
	"region_name": "ap-northeast-2"
	"product_family": "Compute Instance",
	"sku": "22PQKJ49ZN4WMT4U",
	"attributes": {
        "enhancedNetworkingSupported": "Yes", 
        "intelTurboAvailable": "No", 
        "memory": "976 GiB", 
        "dedicatedEbsThroughput": "3500 Mbps", 
        "vcpu": "32", 
        "capacitystatus": "UnusedCapacityReservation", 
        "locationType": "AWS Region", 
        "storage": "1 x 960 SSD", 
        "instanceFamily": "Memory optimized", 
        "operatingSystem": "Windows", 
        "intelAvx2Available": "Yes", 
        "physicalProcessor": "High Frequency Intel Xeon E7-8880 v3 (Haswell)", 
        "clockSpeed": "2.3 GHz", 
        "ecu": "91", 
        "networkPerformance": "Up to 10 Gigabit", 
        "servicename": "Amazon Elastic Compute Cloud", 
        "instancesku": "NWFTMZTA6RK6U7P7", 
        "instanceType": "x1e.8xlarge", 
        "tenancy": "Shared", 
        "usagetype": "APN2-UnusedBox:x1e.8xlarge", 
        "normalizationSizeFactor": "64", 
        "intelAvxAvailable": "Yes", 
        "processorFeatures": "Intel AVX; Intel AVX2", 
        "servicecode": "AmazonEC2", 
        "licenseModel": "No License required", 
        "currentGeneration": "Yes", 
        "preInstalledSw": "NA", 
        "location": "Asia Pacific (Seoul)", 
        "processorArchitecture": "64-bit", 
        "operation": "RunInstances:0002"
    },
    "publication_date": "2021-02-24T06:41:33Z",
    "version": "20210224064133",
    "terms": [{
        "effective_date": "2021-02-01T00:00:00Z", 
        "offer_term_code": "JRTCKXETXF", 
        "term_type": "OnDemand", 
        "price_dimensions": [{
            "price_dimension_code": "6YS6EN2CT7"
            "unit": "Hrs", 
            "end_range": "Inf", 
            "description": "$11.144 per Unused Reservation Windows x1e.8xlarge Instance Hour", 
            "applies_to": [], 
            "rate_code": "22PQKJ49ZN4WMT4U.JRTCKXETXF.6YS6EN2CT7", 
            "begin_range": "0", 
            "price_per_unit": {"USD": "11.1440000000"}, 
            "price_dimension_code": "6YS6EN2CT7"
        }], 
        "term_attributes": {}
    }]
	....
}
~~~
