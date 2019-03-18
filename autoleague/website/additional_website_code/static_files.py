from rlbottraining.history.website.server import make_static_file_aggregator
from autoleague.paths import PackageFiles

from rlbottraining.history.website.view import Aggregator

StaticFileAggregator = make_static_file_aggregator(PackageFiles.additional_website_static)
