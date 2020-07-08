import nlp


class Text(nlp.GeneratorBasedBuilder):
    def _info(self):
        return nlp.DatasetInfo(features=nlp.Features({"text": nlp.Value("string"),}))

    def _split_generators(self, dl_manager):
        """ The `datafiles` kwarg in load_dataset() can be a str, List[str], Dict[str,str], or Dict[str,List[str]].

            If str or List[str], then the dataset returns only the 'train' split.
            If dict, then keys should be from the `nlp.Split` enum.
        """
        if isinstance(self.config.data_files, (str, list, tuple)):
            # Handle case with only one split
            files = self.config.data_files
            if isinstance(files, str):
                files = [files]
            return [nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"files": files})]
        else:
            # Handle case with several splits and a dict mapping
            splits = []
            for split_name in [nlp.Split.TRAIN, nlp.Split.VALIDATION, nlp.Split.TEST]:
                if split_name in self.config.data_files:
                    files = self.config.data_files[split_name]
                    if isinstance(files, str):
                        files = [files]
                    splits.append(nlp.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
            return splits

    def _generate_examples(self, files):
        """ Read files sequentially, then lines sequentially. """
        idx = 0
        for filename in files:
            with open(filename) as file:
                for line in file:
                    yield idx, {"text": line}
                    idx += 1
